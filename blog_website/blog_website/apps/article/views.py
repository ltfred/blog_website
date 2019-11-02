import datetime
import time
from django import http
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from article.models import Article, ArticleCategory, Label
from blog_website.utils import constants
from blog_website.utils.common import get_ip, paginator_function, str2datetime
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
        # 获取上一条数据和下一条数据
        context['next_article'] = self.get_next_article(article)
        context['pre_article'] = self.get_pre_article(article)
        # 相关数据10条
        context['articles'] = self.get_connected_article(article)
        # 阅读次数+1
        article.read_count += 1
        article.save()

        context['article'] = article

        return render(request, 'info.html', context=context)

    def get_next_article(self, article):
        next_article = Article.objects.filter(id__gt=article.id, category2=article.category2).only('id',
                                                                                                   'title').first()
        return next_article

    def get_pre_article(self, article):
        pre_article = Article.objects.filter(id__lt=article.id, category2=article.category2).only('id',
                                                                                                  'title').order_by(
            '-id').first()
        return pre_article

    def get_connected_article(self, article):
        articles = Article.objects.filter(category2=article.category2).only('id', 'title')[0:9]
        return articles


class ArticleTopView(View):
    """点击排行"""

    def get(self, request):

        try:
            articles = Article.objects.order_by('-read_count').all().only('id', 'title')[0:7]
        except Exception as e:
            logger.error('ArticleTopView:get:' + str(e))
            raise Http404
        top_list = [{'title': article.title, 'id': article.id} for article in articles]

        return http.JsonResponse({'code': RETCODE.OK, 'top_list': top_list})


class RecommendView(View):
    """站长推荐"""

    def get(self, request):

        try:
            articles = Article.objects.filter(is_top=True).only('id', 'title', 'index_image')[0:6]
        except Exception as e:
            logger.error('RecommendView:get:' + str(e))
            # return http.HttpResponse('数据库错误')
            raise Http404
        recommend_list = [{'title': article.title, 'id': article.id, 'index_image': article.index_image} for article in
                          articles]

        return http.JsonResponse({'code': RETCODE.OK, 'recommend_list': recommend_list})


class ArticleCountView(View):
    """获取文章数量和pv"""

    def get(self, request):

        conn = get_redis_connection('default')
        pv = conn.get('24_hours_pv')
        now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        now_time = str2datetime(now_time)
        begin_time = str2datetime('2019-08-29')
        days = (now_time - begin_time).days

        try:
            count = Article.objects.count()
        except Exception as e:
            logger.error('ArticleCountView:get:' + str(e))
            # return http.HttpResponse('数据库错误')
            raise Http404
        return http.JsonResponse({'code': RETCODE.OK, 'article_count': count, 'pv': int(pv), 'days': days})


class AllArticleView(View):
    """文章归档"""

    def get(self, request, page_num):
        context = {}
        try:
            articles = Article.objects.order_by('-create_time').all().only('id', 'title')
            context['all_counts'] = articles.count()
        except Exception as e:
            logger.error('AllArticleView:get:' + str(e))
            raise Http404
        context['page_articles'], context['total_page'] = paginator_function(articles, page_num, constants.ARTICLE_LIST_LIMIT)
        context['page_num'] = page_num
        return render(request, 'time.html', context=context)


class CategoryAllArticleView(View):
    """当前类别下的所有文章"""

    def get(self, request, category_id, page_num):
        try:
            # 查出该类别
            category = ArticleCategory.objects.get(id=category_id)
            # 获取文章及数量
            articles, category_article_count = self.get_articles(category)
        except Exception as e:
            logger.error('CategoryAllArticleView:get:' + str(e))
            # return http.HttpResponse('数据库错误')
            raise Http404
        page_query_set, total_page = paginator_function(articles, page_num, constants.ARTICLE_LIST_LIMIT)
        article_labels = []
        for article in page_query_set:
            # 该文章的标签
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
            'page_num': page_num
        }

        context = {'data': data_dict}

        return render(request, 'list.html', context=context)

    def get_articles(self, category):
        # 判断是否为一级分类
        if category.parent is None:
            # 获取一级下的所有文章
            articles = Article.objects.filter(category1=category).order_by('-create_time')
        else:
            # 为二级分类，二级类下的所有文章
            articles = Article.objects.filter(category2=category).order_by('-create_time')
        category_article_count = articles.count()
        return articles, category_article_count


class LabelView(View):
    """获取标签"""

    def get(self, request):

        try:
            # 获取所有标签
            labels_queryset = Label.objects.all()
        except Exception as e:
            logger.error('LabelView:get:' + str(e))
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '获取标签失败'})

        labels = []
        for label in labels_queryset:
            labels.append({
                'id': label.id,
                'name': label.name,
                'article_count': label.article_set.all().count()  # 每个标签下的文章的数量
            })

        return http.JsonResponse({'code': RETCODE.OK, 'labels': labels})


class LabelArticlesView(View):
    """获取该标签下所有文章"""

    def get(self, request, label_id, page_num):

        try:
            label = Label.objects.get(id=label_id)
        except Exception as e:
            logger.error('LabelArticlesView:get:' + str(e))
            # return http.JsonResponse('标签错误')
            raise Http404
        # 查出该标签下所有文章
        articles, article_count = self.get_label_articles(label)
        page_query_set, total_page = paginator_function(articles, page_num, constants.ARTICLE_LIST_LIMIT)
        article_labels = []
        for article in page_query_set:
            # 该文章的标签
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
            'page_num': page_num
        }
        return render(request, 'labelList.html', context=context)

    def get_label_articles(self, label):

        articles = label.article_set.all().order_by('-create_time')
        article_count = articles.count()
        return articles, article_count


class ArticleLikeView(View):
    """文章点赞"""

    def get(self, request, article_id):

        try:
            # 查出该文章
            article = Article.objects.get(id=article_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '获取文章失败'})
        ip = get_ip(request)
        redis = get_redis_connection('default')
        key = 'like_{}_flag_{}'.format(article_id, ip)
        if redis.get(key):
            return http.JsonResponse({'code': RETCODE.ALLOWERR, 'errmsg': '只能点赞一次'})
        # 24小时内只能点赞一次
        redis.set(key, 'article_stars', constants.ARTICLE_STARS_EXPIRE)
        # 文章点赞次数+1
        article.like_count += 1
        article.save()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
