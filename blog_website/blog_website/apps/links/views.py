import random
from django import http
from django.http import Http404
from django.shortcuts import render
from django.views import View

from blog_website.utils.common import get_cat_lst, get_photo_category
from links.models import Link
import logging
from soup.models import Soup

logger = logging.getLogger('blog')


class LinkView(View):
    """友情链接"""

    def get(self, request):
        context = dict()
        try:
            context['recommend_links'] = Link.objects.filter(is_recommend=True)
            context['links'] = Link.objects.filter(is_recommend=False)
            # 分类信息
            context['cat_list'] = get_cat_lst()
            # 相册分类
            context['photo_category'] = get_photo_category()
            # 随机一句心灵鸡汤
            soups = Soup.objects.all()
            context['soup'] = random.choice(soups).content if soups else ''
        except Exception as e:
            logger.error('LinkView:get:' + str(e))
            raise Http404

        return render(request, 'link.html', context=context)
