import datetime
import time
from django import http
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection
from article.models import Article, ArticleCategory, Label
from blog_website.utils import constants
from blog_website.utils.paginator import paginator_function
from blog_website.utils.response_code import RETCODE
import logging

logger = logging.getLogger('blog')


class ArticleDetailView(View):
    """文章详情"""

    def get(self, request, article_id):
        context = {}
        try:
            # 获取本条数据
            article = Article.objects.get(id=article_id)
            # 获取上一条数据和下一条数据
            context['next_article'] = self.get_next_article(article)
            context['pre_article'] = self.get_pre_article(article)
            # 相关数据10条
            context['articles'] = self.get_connected_article(article)
            # 阅读次数+1
            article.read_count += 1
            article.save()
        except Exception as e:
            logger.error(e)
            # return http.HttpResponse('获取文章失败')
            raise Http404
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
            logger.error(e)
            # return http.HttpResponse('数据库错误')
            raise Http404
        top_list = [{'title': article.title, 'id': article.id} for article in articles]

        return http.JsonResponse({'code': RETCODE.OK, 'top_list': top_list})


class RecommendView(View):
    """站长推荐"""

    def get(self, request):

        try:
            articles = Article.objects.filter(is_top=True).only('id', 'title', 'index_image')[0:6]
        except Exception as e:
            logger.error(e)
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
        now_time = datetime.datetime.strptime(now_time, '%Y-%m-%d')
        begin_time = datetime.datetime.strptime('2019-08-29', '%Y-%m-%d')
        days = (now_time - begin_time).days

        try:
            count = Article.objects.count()
        except Exception as e:
            logger.error(e)
            # return http.HttpResponse('数据库错误')
            raise Http404
        return http.JsonResponse({'code': RETCODE.OK, 'article_count': count, 'pv': int(pv), 'days': days})


class AllArticleView(View):
    """文章归档"""

    def get(self, request, page_num):

        try:
            articles = Article.objects.order_by('-create_time').all().only('id', 'title')
            all_counts = articles.count()
        except Exception as e:
            logger.error(e)
            # return http.HttpResponse('数据库错误')
            raise Http404
        # 分页
        paginator = Paginator(articles, constants.ARTICLE_LIST_LIMIT)
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            # return http.HttpResponseNotFound('empty page')
            raise Http404
        # 获取列表页总页数
        total_page = paginator.num_pages
        context = {
            'page_num': page_num,
            'total_page': total_page,
            'page_articles': page_articles,
            'all_counts': all_counts

        }

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
            logger.error(e)
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

        return render(request, 'list2_1.html', context=context)

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
            logger.error(e)
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
            logger.error(e)
            # return http.JsonResponse('标签错误')
            raise Http404
        try:
            # 查出该标签下所有文章
            articles = label.article_set.all().order_by('-create_time')
            article_count = articles.count()
        except Exception as e:
            logger.error(e)
            # return http.JsonResponse('获取文章失败')
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

        context = {
            'label': label,
            'articles': article_labels,
            'article_count': article_count,
            'total_page': total_page,
            'page_num': page_num
        }
        return render(request, 'label_list.html', context=context)


class ArticleLikeView(View):
    """文章点赞"""

    def get(self, request, article_id):

        try:
            # 查出该文章
            article = Article.objects.get(id=article_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '获取文章失败'})

        # 获取请求的ip
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP

        redis = get_redis_connection('default')
        key = 'like_{}_flag_{}'.format(article_id, ip)
        if redis.get(key):
            return http.JsonResponse({'code': RETCODE.ALLOWERR, 'errmsg': '只能点击一次'})
        # 24小时内只能点赞一次
        redis.set(key, 'article_stars', constants.ARTICLE_STARS_EXPIRE)
        # 文章点赞次数+1
        article.like_count += 1
        article.save()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
