from django import http
from django.shortcuts import render
from django.views import View

from blog_website.utils.response_code import RETCODE
from user.models import User


class UserProfileView(View):
    """获取用户信息"""

    def get(self, request):

        try:
            user = User.objects.get(id=1)
        except Exception as e:
            return http.HttpResponse('数据库错误')

        profile = {
            'username': user.username,
            'profession': user.profession,
            'address': user.address,
            'email': user.email
        }

        return http.JsonResponse({'code': RETCODE.OK, 'profile': profile})


class AboutUserView(View):
    """关于我"""

    def get(self, request):

        try:
            user = User.objects.get(id=1)
        except Exception as e:
            return http.HttpResponse('数据库错误')

        context = {'bio': user.bio, 'dubai': user.soliloquy, 'name': user.username,
                   'avatar': user.avatar_url }

        return render(request, 'about.html', context=context)
