import random
from django import http
from django.http import Http404
from django.shortcuts import render
from django.views import View
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
            # 随机一句心灵鸡汤
            soups = Soup.objects.all()
            context['soup'] = random.choice(soups).content if soups else ''
        except Exception as e:
            logger.error('LinkView:get:' + str(e))
            raise Http404

        return render(request, 'daohang.html', context=context)
