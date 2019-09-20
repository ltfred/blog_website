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
        except Exception as e:
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
        except Exception as e:
            return http.HttpResponse('数据库错误')

        top_list = [{'title': article.title, 'id': article.id} for article in articles]

        return http.JsonResponse({'code': RETCODE.OK, 'top_list': top_list})


class RecommendView(View):
    """站长推荐"""

    def get(self, request):

        try:
            articles = Article.objects.filter(is_top=True)[0:6]
        except Exception as e:
            return http.HttpResponse('数据库错误')

        recommend_list = [{'title': article.title, 'id': article.id, 'index_image': article.index_image} for article in
                          articles]

        return http.JsonResponse({'code': RETCODE.OK, 'recommend_list': recommend_list})


class ArticleCountView(View):
    """获取文章数量"""
    def get(self, request):

        try:
            count = Article.objects.count()
        except Exception as e:
            return http.HttpResponse('数据库错误')

        return http.JsonResponse({'code': RETCODE.OK, 'article_count': count})

