from django import http
from django.shortcuts import render
from django.views import View
from article.models import Article, ArticleCategory
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


class AllArticleView(View):
    """所有文章"""

    def get(self, request):

        try:
            articles = Article.objects.order_by('-create_time').all()
        except Exception as e:
            return http.HttpResponse('数据库错误')

        article_list = []
        for article in articles:
            article_list.append({
                'id': article.id,
                'title': article.title,
                'create_time': article.create_time
            })
        context = {'all_article': article_list}

        return render(request, 'time.html', context=context)


class CategoryAllArticleView(View):
    """当前类别下的所有文章"""

    def get(self, request, category_id):

        try:
            category = ArticleCategory.objects.get(id=category_id)
        except Exception as e:
            return http.HttpResponse('数据库错误')
        # 判断是否为一级分类
        if category.parent is None:
            articles = Article.objects.filter(category1=category)

            data_dict = {}
            cat2_list = ArticleCategory.objects.filter(parent__isnull=False)

            data_dict['categories'] = []

            for cat2 in cat2_list:
                data_dict['categories'].append({
                    'id': cat2.id,
                    'name': cat2.name
                })
            data_dict['articles'] = articles

            data_dict['category'] = category.name

        else:
            # 为二级分类
            articles = Article.objects.filter(category2=category)

            cat2_list = ArticleCategory.objects.filter(parent__isnull=False)

            category2_list = []

            for cat2 in cat2_list:
                category2_list.append({
                    'id': cat2.id,
                    'name': cat2.name
                })
            # data_dict['articles'] = articles
            #
            # data_dict['category'] = category.name

            data_dict = {
                'category': category.name,
                'categories': category2_list,
                'articles': articles
            }

        context = {'data': data_dict}

        return render(request, 'list2_1.html', context=context)
