from django import http
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import TemplateView
from blog_website.utils import constants
from blog_website.utils.common import get_image_size, paginator_function, get_cat_lst, get_photo_category, get_labels, \
    get_top, get_recommend
from blog_website.utils.responseCode import RETCODE
from photo.models import PhotoCategory, Photo
import logging
from user.models import User

logger = logging.getLogger('blog')


class PhotoCategoryView(View):
    """相册分类"""

    def get(self, request):
        photo_categories = get_photo_category()
        return http.JsonResponse({'code': RETCODE.OK, 'photo_categories': photo_categories})


class AllPhotosView(View):
    """获取所有照片"""

    def get(self, request, page_num):
        try:
            if request.user.is_anonymous:
                photo_query_set = Photo.objects.filter(category__is_secret=False).order_by('-create_time')
            else:
                photo_query_set = Photo.objects.all().order_by('-create_time')
        except Exception as e:
            logger.error(e)
            raise
        page_photos, total_page = paginator_function(photo_query_set, page_num, constants.PHOTO_LIST_LIMIT)
        context = {
            'photos': page_photos,
            'total_page': total_page,
            'page_num': page_num,
            'cat_list': get_cat_lst(),
            'photo_category': get_photo_category()
        }

        return render(request, 'photo.html', context=context)


class CategoryPhotoView(View):
    """获取该类别下的所有照片"""

    def get(self, request, category_id, page_num):
        photoCategory = PhotoCategory.objects.get(id=category_id)
        if photoCategory.is_secret == True and request.user.is_anonymous:
            url = request.get_full_path()
            res = render(request, 'login.html')
            res.set_cookie('next', url)
            return res
        try:
            photos = Photo.objects.filter(category_id=category_id).order_by('-create_time')
        except Exception as e:
            logger.error(e)
            raise
        page_photos, total_page = paginator_function(photos, page_num, constants.PHOTO_LIST_LIMIT)

        context = {
            'category_id': category_id,
            'photos': page_photos,
            'total_page': total_page,
            'page_num': page_num,
            'cat_list': get_cat_lst(),
            'photo_category': get_photo_category()
        }

        return render(request, 'categoryPhoto.html', context=context)


class PhotoDetailView(TemplateView):
    template_name = 'photoDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        photo_id = self.request.GET.get('photo_id')
        photo = Photo.objects.get(id=photo_id)
        try:
            size = get_image_size(photo.url)
        except:
            size = ''
        user = User.objects.get(is_staff=True)
        context['recommend_list'] = get_recommend()
        context['top_list'] = get_top()
        context['labels'] = get_labels()
        context['photo'] = photo
        context['size'] = size
        context['webname'] = user.webname
        context['avatar'] = user.avatar_url
        context['cat_list'] = get_cat_lst()
        context['photo_category'] = get_photo_category()
        return context

