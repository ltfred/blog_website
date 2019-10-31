from django import http
from django.http import Http404
from django.shortcuts import render
from django.views import View
from blog_website.utils.response_code import RETCODE
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
                   'avatar': user.avatar_url}

        return render(request, 'about.html', context=context)
