from blog_website.utils.constants import Const
from django import http
from django.shortcuts import render
from django.views import View

from article.models import ArticleCategory
from blog_website.utils.common import paginator_function, get_photo_category
from blog_website.utils.responseCode import RETCODE
from photo.models import PhotoCategory, Photo, PhotoGroup
import logging

logger = logging.getLogger('blog')


class PhotoCategoryView(View):
    """相册分类"""

    def get(self, request):
        photo_categories = get_photo_category()
        return http.JsonResponse({'code': RETCODE.OK, 'photo_categories': photo_categories})


class PhotoGroupView(View):
    """获取照片组"""

    def get(self, request, page_num):
        try:
            if request.user.is_anonymous:
                photo_groups = PhotoGroup.objects.filter(category__is_secret=False).order_by('-create_time')
            else:
                photo_groups = Photo.objects.all().order_by('-create_time')
        except Exception as e:
            logger.error(e)
            raise
        page_photo_groups, total_page = paginator_function(photo_groups, page_num, Const.EXTREMUM.PHOTO_LIST)
        context = {
            'photo_groups': page_photo_groups,
            'total_page': total_page,
            'page_num': page_num,
            'cat_list': ArticleCategory.get_cat_lst(),
            'photo_group_count': photo_groups.count(),
            'photo_category': get_photo_category()
        }

        return render(request, 'photo.html', context=context)


class CategoryPhotoGroupView(View):
    """获取该类别下的所有照片组"""

    def get(self, request, category_id, page_num):
        photo_category = PhotoCategory.objects.get(id=category_id)
        if photo_category.is_secret is True and request.user.is_anonymous:
            url = request.get_full_path()
            res = render(request, 'login.html')
            res.set_cookie('next', url)
            return res
        try:
            photo_groups = PhotoGroup.objects.filter(category=photo_category).order_by('-create_time')
        except Exception as e:
            logger.error(e)
            raise
        page_photo_groups, total_page = paginator_function(photo_groups, page_num, Const.EXTREMUM.PHOTO_LIST)

        context = {
            'category_id': category_id,
            'photo_groups': page_photo_groups,
            'total_page': total_page,
            'page_num': page_num,
            'cat_list': ArticleCategory.get_cat_lst(),
            'photo_group_count': photo_groups.count(),
            'photo_category': get_photo_category()
        }

        return render(request, 'categoryPhoto.html', context=context)


class Photos(View):
    """获取分组下的所有照片"""

    def get(self, request, group_id):
        group = PhotoGroup.objects.get(id=group_id)
        photos = Photo.objects.filter(group_id=group_id)
        return render(request, "photos.html", {"photos": photos, "group": group})

