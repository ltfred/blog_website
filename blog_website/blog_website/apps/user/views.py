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