from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from links.models import Link


class LinkView(View):
    """友情链接"""
    def get(self, request):

        try:
            recommend_links = Link.objects.filter(is_recommend=True)
            links = Link.objects.filter(is_recommend=False)
        except Exception as e:
            return http.HttpResponse('获取界面失败')

        context = {'recommend_links': recommend_links, 'links': links}

        return render(request, 'daohang.html', context=context)
