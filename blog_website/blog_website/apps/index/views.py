import random
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from rest_framework.views import APIView
from article.models import Article, ArticleCategory
from blog_website.utils.response_code import RETCODE
import logging

logger = logging.getLogger('blog')


class IndexView(View):
    """返回首页"""

    def get(self, request):

        # 24小时内PV记录
        conn = get_redis_connection('default')
        if conn.setnx('24_hours_pv', 0):
            conn.expire('24_hours_pv', 24 * 60 * 60)
        conn.incr('24_hours_pv')

        # 最新博文
        try:
            articles = Article.objects.order_by('-create_time')[0:10]
        except Exception as e:
            logger.error(e)
            return http.HttpResponse('数据库错误')
        article_labels = []
        for article in articles:
            # 该文章的标签
            labels = article.labels.all()
            article_labels.append({
                'article': article,
                'labels': labels
            })

        # 分类信息
        try:
            cat1_list = ArticleCategory.objects.filter(parent__isnull=True)
        except Exception as e:
            logger.error(e)
            return http.HttpResponse('数据库错误')
        cat_list = []
        for cat1 in cat1_list:
            cat2_list = ArticleCategory.objects.filter(parent=cat1)
            subs = [{'id': cat2.id, 'name': cat2.name} for cat2 in cat2_list]

            cat_list.append({
                'id': cat1.id,
                'name': cat1.name,
                'subs': subs
            })

        # 轮播图
        try:
            index_images = Article.objects.all().only('id', 'index_image', 'title')
        except Exception as e:
            logger.error(e)
            return http.HttpResponse('数据库错误')
        # 随机选择
        carousel_articles = []
        static_articles = []
        if index_images.count() > 3:
            carousel_articles = random.sample(list(index_images), 3)
            static_articles = random.sample(list(index_images), 2)

        # 精彩专题数据
        like_articles = []
        try:
            like_articles = Article.objects.order_by('-like_count').only('id', 'title', 'index_image', 'describe')[0:6]
        except Exception as e:
            logger.error(e)

        context = {
            'articles': article_labels,
            'cat_list': cat_list,
            'carousel_articles': carousel_articles,
            'static_articles': static_articles,
            'like_articles': like_articles

        }

        return render(request, 'index.html', context=context)


class CategoryView(View):
    """分类"""

    def get(self, request):
        try:
            cat1_list = ArticleCategory.objects.filter(parent__isnull=True)
        except Exception as e:
            logger.error(e)
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
