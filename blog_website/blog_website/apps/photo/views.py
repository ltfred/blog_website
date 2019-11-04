from django import http
from django.http import Http404
from django.shortcuts import render
from django.views import View
from blog_website.utils import constants
from blog_website.utils.common import get_image_size, paginator_function
from blog_website.utils.responseCode import RETCODE
from photo.models import PhotoCategory, Photo
import logging
from user.models import User

logger = logging.getLogger('blog')


class PhotoCategoryView(View):
    """相册分类"""

    def get(self, request):

        try:
            photo_category_query_set = PhotoCategory.objects.all()
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库查询失败'})

        photo_categories = [{'id': photo_category.id, 'name': photo_category.name} for photo_category in
                            photo_category_query_set]

        return http.JsonResponse({'code': RETCODE.OK, 'photo_categories': photo_categories})


class AllPhotosView(View):
    """获取所有照片"""

    def get(self, request, page_num):

        try:
            photo_query_set = Photo.objects.all().order_by('-create_time')
        except Exception as e:
            logger.error(e)
            # return http.HttpResponse('获取照片页失败')
            raise Http404

        page_photos, total_page = paginator_function(photo_query_set, page_num, constants.PHOTO_LIST_LIMIT)

        context = {
            'photos': page_photos,
            'total_page': total_page,
            'page_num': page_num
        }

        return render(request, 'photo.html', context=context)


class CategoryPhotoView(View):
    """获取该类别下的所有照片"""

    def get(self, request, category_id, page_num):

        try:
            photos = Photo.objects.filter(category_id=category_id).order_by('-create_time')
        except Exception as e:
            logger.error(e)
            # return http.HttpResponse('获取照片失败')
            raise Http404
        page_photos, total_page = paginator_function(photos, page_num, constants.PHOTO_LIST_LIMIT)

        context = {
            'category_id': category_id,
            'photos': page_photos,
            'total_page': total_page,
            'page_num': page_num
        }

        return render(request, 'categoryPhoto.html', context=context)


class PhotoDetailView(View):

    def get(self, request):
        id = request.GET.get('photo_id')
        photo = Photo.objects.get(id=id)
        try:
            size = get_image_size(photo.url)
        except:
            size = ''
        user = User.objects.get(is_staff=True)
        return render(request, 'photoDetail.html', context={'photo': photo, 'size': size, 'user': user})