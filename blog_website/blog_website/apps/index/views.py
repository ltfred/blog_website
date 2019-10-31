import random
from django import http
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from article.models import Article, ArticleCategory
from blog_website.utils import constants
from blog_website.utils.response_code import RETCODE
import logging
from index.models import Carousel
from user.models import User

logger = logging.getLogger('blog')


class IndexView(View):
    """返回首页"""

    def get(self, request):
        # 24小时内PV记录
        conn = get_redis_connection('default')
        if conn.setnx('24_hours_pv', 0):
            conn.expire('24_hours_pv', constants.PV_EXPIRE)
        conn.incr('24_hours_pv')
        context = {}
        # 最新博文
        context['article_labels'] = self.get_new_articles()
        # 分类信息
        context['cat_list'] = self.get_cat_lst()
        # 静态随机图
        context['static_articles'] = self.get_static_articles()
        # 轮播图
        context['carousel_articles'] = self.get_carousel_articles()
        # 精彩专题数据
        context['like_articles'] = self.get_like_articles()
        # 个人信息
        context['profile'] = self.get_profile()

        return render(request, 'index.html', context=context)

    def get_profile(self):
        user = User.objects.all()[0]
        profile = {
            'webname': user.webname,
            'profession': user.profession,
            'address': user.address,
            'email': user.email
        }
        return profile

    def get_like_articles(self):
        like_articles = Article.objects.order_by('-like_count').only('id', 'title', 'index_image', 'describe')[0:6]
        return like_articles

    def get_carousel_articles(self):
        carousel_articles = Carousel.objects.filter(is_active=True)
        return carousel_articles

    def get_static_articles(self):
        index_images = Article.objects.all().only('id', 'index_image', 'title')
        # 随机选择
        static_articles = []
        if index_images.count() > 3:
            static_articles = random.sample(list(index_images), 2)
        return static_articles

    def get_cat_lst(self):

        cat1_list = ArticleCategory.objects.filter(parent__isnull=True)
        cat_list = []
        for cat1 in cat1_list:
            cat2_list = ArticleCategory.objects.filter(parent=cat1)
            subs = [{'id': cat2.id, 'name': cat2.name} for cat2 in cat2_list]

            cat_list.append({
                'id': cat1.id,
                'name': cat1.name,
                'subs': subs
            })
        return cat_list

    def get_new_articles(self):
        articles = Article.objects.order_by('-create_time')[0:10]
        article_labels = []
        for article in articles:
            # 该文章的标签
            labels = article.labels.all()
            article_labels.append({
                'article': article,
                'labels': labels
            })
        return article_labels

class CategoryView(View):
    """分类"""

    def get(self, request):
        cat_list = IndexView.get_cat_lst()
        return http.JsonResponse({'code': RETCODE.OK, 'cat_list': cat_list})
