from django import http
from django.shortcuts import render
from django.views import View
from article.models import Article
import markdown

from blog_website.utils.response_code import RETCODE


class ArticleDetailView(View):
    """文章详情"""

    def get(self, request, article_id):

        try:
            article = Article.objects.get(id=article_id)
        except:
            return http.HttpResponse('获取文章失败')

        # 阅读次数+1
        article.read_count += 1
        article.save()

        exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
                'markdown.extensions.toc']

        # 将markdown语法渲染成html样式
        article.content = markdown.markdown(article.content, extensions=exts)

        context = {'article': article}

        return render(request, 'info.html', context=context)


class ArticleTopView(View):
    """点击排行"""
    def get(self, request):

        try:
            articles = Article.objects.order_by('-read_count').all()[0:7]
        except:
            return http.HttpResponse('数据库错误')

        top_list = []
        for article in articles:
            top_list.append({
                'title': article.title,
                'id': article.id
            })

        return http.JsonResponse({'code': RETCODE.OK, 'top_list': top_list})