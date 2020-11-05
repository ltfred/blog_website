import random
from django import http
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView

from article.models import ArticleCategory
from blog_website.utils.common import get_photo_category
from user.models import User
import logging

logger = logging.getLogger('blog')


class AboutUserView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.all()[0]
        context['bio'] = user.bio
        context['dubai'] = user.soliloquy
        context['name'] = user.webname
        context['avatar'] = user.avatar_url
        context['cat_list'] = ArticleCategory.get_cat_lst()
        context['photo_category'] = get_photo_category()
        return context


class MusicView(TemplateView):
    template_name = 'player.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_list'] = ArticleCategory.get_cat_lst()
        context['photo_category'] = get_photo_category()
        return context


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            return http.JsonResponse({'code': 400, 'msg': '请填写完整的参数'})
        try:
            user = User.objects.get(username=username)
        except:
            return http.JsonResponse({'code': 401, 'msg': '账号或密码错误'})
        if not user.check_password(password):
            return http.JsonResponse({'code': 401, 'msg': '账号或密码错误'})
        login(request, user)
        next = request.COOKIES.get('next', '/')
        return http.JsonResponse({'code': 200, 'msg': '登录成功', 'next': next})


class ForgetPasswordView(View):

    def post(self, request):
        email = request.POST.get('email')
        if not all([email]):
            return http.JsonResponse({'code': 400, 'msg': '请填写完整的参数'})
        try:
            user = User.objects.get(email=email)
        except:
            return http.JsonResponse({'code': 401, 'msg': '该邮箱未注册'})
        username = user.username
        password = '%09d' % random.randint(0, 999999999)
        user.set_password(password)
        return http.JsonResponse({'code': 201, 'msg': u'你的用户名为：{},密码为：{},请尽快修改密码'.format(username, password)})


class ModifyPasswordView(View):

    def post(self, request):
        oldpassword = request.POST.get('oldpassword')
        newpassword = request.POST.get('newpassword')
        newpassword2 = request.POST.get('newpassword2')
        if not all([oldpassword, newpassword, newpassword2]):
            return http.JsonResponse({'code': 400, 'msg': '请填写完整的参数'})
        if request.user.is_anonymous:
            return http.JsonResponse({'code': 403, 'msg': '请先登录'})
        user = request.user
        if newpassword != newpassword2:
            return http.JsonResponse({'code': 405, 'msg': '两次密码不相同'})
        if not user.check_password(oldpassword):
            return http.JsonResponse({'code': 401, 'msg': '旧密码不正确'})
        user.set_password(newpassword)
        logout(request)
        return redirect(reverse('user:login'))
