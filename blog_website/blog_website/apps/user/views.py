from django import http
from django.http import Http404
from django.shortcuts import render
from django.views import View
from blog_website.utils.common import get_cat_lst, get_photo_category
from blog_website.utils.responseCode import RETCODE
from user.models import User
import logging

logger = logging.getLogger('blog')


class AboutUserView(View):
    """关于我"""

    def get(self, request):

        try:
            user = User.objects.all()[0]
        except Exception as e:
            logger.error(e)
            # return http.HttpResponse('数据库错误')
            raise Http404

        context = {'bio': user.bio, 'dubai': user.soliloquy, 'name': user.webname,
                   'avatar': user.avatar_url, 'cat_list': get_cat_lst(),
                   'photo_category': get_photo_category()}

        return render(request, 'about.html', context=context)


class MusicView(View):

    def get(self, request):
        context = dict()
        context['cat_list'] = get_cat_lst()
        context['photo_category'] = get_photo_category()
        return render(request, 'player.html', context=context)