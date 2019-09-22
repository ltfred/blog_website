import random

from django import http
from django.shortcuts import render
from django.views import View
from links.models import Link
import logging

from soup.models import Soup

logger = logging.getLogger('blog')


class LinkView(View):
    """友情链接"""

    def get(self, request):

        try:
            recommend_links = Link.objects.filter(is_recommend=True)
            links = Link.objects.filter(is_recommend=False)
            # 随机一句心灵鸡汤
            soups = Soup.objects.all()
            soup = random.choice(soups)
        except Exception as e:
            logger.error(e)
            return http.HttpResponse('获取界面失败')

        context = {'recommend_links': recommend_links, 'links': links, 'soup': soup.content}

        return render(request, 'daohang.html', context=context)
