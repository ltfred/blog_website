from django import http
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView
from blog_website.utils.common import get_cat_lst, get_photo_category
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
        context['cat_list'] = get_cat_lst()
        context['photo_category'] = get_photo_category()
        return context


class MusicView(TemplateView):
    template_name = 'player.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cat_list'] = get_cat_lst()
        context['photo_category'] = get_photo_category()
        return context


class LoginView(TemplateView):
    template_name = 'login.html'

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.get(username=username)
        if not user.check_password(password):
            return http.JsonResponse({'code': 401, 'msg': '账号或密码错误'})
        login(request, user)
        return redirect(request.COOKIES.get('next'))

class ForgetPasswordView(View):

    def post(self, request):
        email = request.POST.get('email')
        user = User.objects.get(email=email)
        username = user.username
        user.set_password('123456789')
        return redirect(reverse('user:login'))
