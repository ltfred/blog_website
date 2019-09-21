from django import http
from django.shortcuts import render
from django.views import View
from blog_website.utils.response_code import RETCODE
from photo.models import PhotoCategory, Photo
import logging

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

    def get(self, request):

        try:
            photo_query_set = Photo.objects.all().order_by('-create_time')
        except Exception as e:
            logger.error(e)
            return http.HttpResponse('获取照片页失败')

        context = {'photos': photo_query_set}

        return render(request, 'photo.html', context=context)


class CategoryPhotoView(View):
    """获取该类别下的所有照片"""

    def get(self, request, category_id):

        try:
            photos = Photo.objects.filter(category_id=category_id)
        except Exception as e:
            logger.error(e)
            return http.HttpResponse('获取照片失败')

        context = {'photos': photos}

        return render(request, 'photo.html', context=context)

