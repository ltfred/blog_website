import random
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from article.models import Article, ArticleCategory
from blog_website.utils import constants
from blog_website.utils.common import (
    get_photo_category,
    get_cat_lst,
    get_notice,
    get_recommend,
    get_top,
    get_labels,
    get_site_info
)
from blog_website.utils.responseCode import RETCODE
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
        context = dict()
        context['articles'] = self.get_new_articles()
        context['cat_list'] = self.get_cat_lst()
        context['static_articles'] = self.get_static_articles()
        context['carousel_articles'] = self.get_carousel_articles()
        context['like_articles'] = self.get_like_articles()[0:6]
        context['profile'] = self.get_profile()
        context['photo_category'] = get_photo_category()
        context['notice_list'] = get_notice()
        context['recommend_list'] = get_recommend()
        context['top_list'] = get_top()
        context['labels'] = get_labels()
        context['count'], context['pv'], context['days'] = get_site_info()
        return render(request, 'index.html', context=context)

    @staticmethod
    def get_profile():
        user = User.objects.all()[0]
        profile = dict()
        profile['webname'] = user.webname
        profile['profession'] = user.profession
        profile['address'] = user.address
        profile['email'] = user.email
        return profile

    @staticmethod
    def get_like_articles():
        like_articles = Article.objects.order_by('-like_count').only('id', 'title', 'index_image', 'describe')
        return like_articles

    @staticmethod
    def get_carousel_articles():
        carousel_articles = Carousel.objects.filter(is_active=True)
        return carousel_articles

    def get_static_articles(self):
        index_images = self.get_like_articles()
        static_articles = []
        if index_images.count() > 3:
            static_articles = random.sample(list(index_images), 2)
        return static_articles

    @staticmethod
    def get_cat_lst():

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

    @staticmethod
    def get_new_articles():
        articles = Article.objects.order_by('-create_time')[0:10]
        article_labels = list()
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
        cat_list = get_cat_lst()
        return http.JsonResponse({'code': RETCODE.OK, 'cat_list': cat_list})



