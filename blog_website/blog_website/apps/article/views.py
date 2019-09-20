from django import http
from django.shortcuts import render
from django.views import View
from article.models import Article
import markdown


class ArticleDetailView(View):
    """文章详情"""

    def get(self, request, article_id):

        try:
            article = Article.objects.get(id=article_id)
        except:
            return http.HttpResponse('获取文章失败')

        exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
                'markdown.extensions.toc']

        # 将markdown语法渲染成html样式
        article.content = markdown.markdown(article.content, extensions=exts)

        context = {'article': article}

        return render(request, 'info.html', context=context)
