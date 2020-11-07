from blog_website.utils.constants import Const
import random
from django import http
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from article.models import Article, ArticleCategory
from blog_website.utils import constants
from blog_website.utils.common import get_photo_category, get_notice, get_recommend, get_top, get_labels, \
    get_site_info
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
            conn.expire('24_hours_pv', Const.EXTREMUM.PV_EXPIRE)
        conn.incr('24_hours_pv')
        context = dict()
        context['articles'] = Article.get_new_articles()
        context['cat_list'] = ArticleCategory.get_cat_lst()
        context['static_articles'] = Article().get_static_articles()
        context['carousel_articles'] = Carousel.get_carousel_articles()
        context['like_articles'] = Article.get_like_articles()[0:6]
        context['profile'] = User.get_profile()
        context['photo_category'] = get_photo_category()
        context['notice_list'] = get_notice()
        context['recommend_list'] = get_recommend()
        context['top_list'] = get_top()
        context['labels'] = get_labels()
        context['count'], context['pv'], context['days'] = get_site_info()
        return render(request, 'index.html', context=context)


class CategoryView(View):
    """分类"""

    def get(self, request):
        cat_list = ArticleCategory.get_cat_lst()
        return http.JsonResponse({'code': RETCODE.OK, 'cat_list': cat_list})



