import markdown
from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View

from article.models import Article, ArticleCategory
from blog_website.utils.response_code import RETCODE


class IndexView(View):
    """返回首页"""

    def get(self, request):

        try:
            articles = Article.objects.order_by('create_time')[0:9]
        except Exception as e:
            return http.HttpResponse('数据库错误')

        try:
            cat1_list = ArticleCategory.objects.filter(parent__isnull=True)
        except Exception as e:
            return http.HttpResponse('数据库错误')

        cat_list = []
        for cat1 in cat1_list:
            cat2_list = ArticleCategory.objects.filter(parent=cat1)
            subs = []
            for cat2 in cat2_list:
                subs.append({
                    'id': cat2.id,
                    'name': cat2.name
                })

            cat_list.append({
                'id': cat1.id,
                'name': cat1.name,
                'subs': subs
            })
        context = {'articles': articles, 'cat_list': cat_list}

        return render(request, 'index.html', context=context)


class CategoryView(View):
    """分类"""
    def get(self, request):
        try:
            cat1_list = ArticleCategory.objects.filter(parent__isnull=True)
        except Exception as e:
            return http.HttpResponse('数据库错误')

        cat_list = []
        for cat1 in cat1_list:
            cat2_list = ArticleCategory.objects.filter(parent=cat1)
            subs = []
            for cat2 in cat2_list:
                subs.append({
                    'id': cat2.id,
                    'name': cat2.name
                })

            cat_list.append({
                'id': cat1.id,
                'name': cat1.name,
                'subs': subs
            })

        return http.JsonResponse({'code': RETCODE.OK, 'cat_list': cat_list})