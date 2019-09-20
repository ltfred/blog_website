import markdown
from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from article.models import Article
from blog_website.utils.response_code import RETCODE


class IndexView(View):
    """返回首页"""

    def get(self, request):

        try:
            articles = Article.objects.order_by('create_time')[0:9]
        except:
            return http.HttpResponse('数据库错误')
        context = {'articles': articles}

        return render(request, 'index.html', context=context)
