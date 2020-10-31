from django import http
from django.http import HttpResponse, Http404
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from haystack.views import SearchView
from article.models import Article, ArticleCategory, Label
from blog_website.utils import constants
from blog_website.utils.common import (
    paginator_function,
    get_cat_lst,
    get_photo_category,
    get_recommend,
    get_top,
    get_labels,
    get_site_info, get_ip, increase_view_count
)
from blog_website.utils.responseCode import RETCODE
import logging

logger = logging.getLogger('blog')


class ArticleDetailView(View):
    """文章详情"""

    def get(self, request, article_id):
        context = {}
        try:
            # 获取本条数据
            article = Article.objects.get(id=article_id)
        except Exception as e:
            logger.error('ArticleDetailView:get:' + str(e))
            raise Http404
        increase_view_count(request, article)
        context['next_article'] = article.get_next_article()
        context['pre_article'] = article.get_pre_article()
        context['articles'] = article.get_connected_article()
        context['article'] = article
        context['cat_list'] = get_cat_lst()
        context['photo_category'] = get_photo_category()
        context['recommend_list'] = get_recommend()
        context['top_list'] = get_top()
        context['labels'] = get_labels()
        return render(request, 'info.html', context=context)


class ArticleTopView(View):
    """点击排行"""

    def get(self, request):
        top_list = get_top()
        return http.JsonResponse({'code': RETCODE.OK, 'top_list': top_list})


class RecommendView(View):
    """站长推荐"""

    def get(self, request):
        recommend_list = get_recommend()
        return http.JsonResponse({'code': RETCODE.OK, 'recommend_list': recommend_list})


class ArticleCountView(View):
    """获取文章数量和pv"""

    def get(self, request):
        count, pv, days = get_site_info()
        return http.JsonResponse({'code': RETCODE.OK, 'article_count': count, 'pv': pv, 'days': days})


class AllArticleView(View):
    """文章归档"""

    def get(self, request, page_num):
        context = {}
        try:
            articles = Article.objects.order_by('-create_time').all().only('id', 'title')
            context['all_counts'] = articles.count()
        except Exception as e:
            logger.error('AllArticleView:get:' + str(e))
            raise
        context['page_articles'], context['total_page'] = paginator_function(
            articles, page_num, constants.HISTORY_ARTICLE_LIST_LIMIT
        )
        context['page_num'] = page_num
        # 分类信息
        context['cat_list'] = get_cat_lst()
        # 相册分类
        context['photo_category'] = get_photo_category()
        return render(request, 'time.html', context=context)


class CategoryAllArticleView(View):
    """当前类别下的所有文章"""

    def get(self, request, category_id, page_num):
        try:
            category = ArticleCategory.objects.get(id=category_id)
            articles, category_article_count = category.get_articles()
        except Exception as e:
            logger.error('CategoryAllArticleView:get:' + str(e))
            raise
        page_query_set, total_page = paginator_function(articles, page_num, constants.ARTICLE_LIST_LIMIT)
        article_labels = []
        for article in page_query_set:
            labels = article.labels.all()
            article_labels.append({
                'article': article,
                'labels': labels
            })

        data_dict = {
            'category_id': category.id,
            'articles': article_labels,
            'category': category,
            'article_count': category_article_count,
            'total_page': total_page,
            'page_num': page_num,
            'cat_list': get_cat_lst(),
            'photo_category': get_photo_category(),
            'recommend_list': get_recommend(),
            'top_list': get_top(),
            'labels': get_labels(),
        }
        return render(request, 'list.html', context=data_dict)


class LabelView(View):
    """获取标签"""

    def get(self, request):
        labels = get_labels()
        return http.JsonResponse({'code': RETCODE.OK, 'labels': labels})


class LabelArticlesView(View):
    """获取该标签下所有文章"""

    def get(self, request, label_id, page_num):

        try:
            label = Label.objects.get(id=label_id)
        except Exception as e:
            logger.error('LabelArticlesView:get:' + str(e))
            raise
        articles, article_count = label.get_label_articles()
        page_query_set, total_page = paginator_function(articles, page_num, constants.ARTICLE_LIST_LIMIT)
        article_labels = []
        for article in page_query_set:
            labels = article.labels.all()
            article_labels.append({
                'article': article,
                'labels': labels
            })

        context = {
            'label': label,
            'articles': article_labels,
            'article_count': article_count,
            'total_page': total_page,
            'page_num': page_num,
            'cat_list': get_cat_lst(),
            'photo_category': get_photo_category(),
            'recommend_list': get_recommend(),
            'top_list': get_top(),
            'labels': get_labels(),
        }

        return render(request, 'labelList.html', context=context)


class ArticleLikeView(View):
    """文章点赞"""
    def post(self, request, article_id):
        article_obj = Article.objects.get(id=article_id)
        article_obj.like_count += 1
        article_obj.save()
        return HttpResponse('success')


class ArticleSearchView(SearchView):
    template = 'search.html'

    def get_total_page(self):
        paginator, page = self.build_page()
        return paginator.num_pages

    def extra_context(self):
        content = super(ArticleSearchView, self).extra_context()
        content['cat_list'] = get_cat_lst()
        content['photo_category'] = get_photo_category()
        content['total_count'] = self.results.count()
        content["page_num"] = int(self.request.GET.get('page', 1))
        content["total_page"] = self.get_total_page()
        return content

