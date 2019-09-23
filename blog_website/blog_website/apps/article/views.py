from django import http
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

from article.models import Article, ArticleCategory
import markdown
from blog_website.utils import constants
from blog_website.utils.response_code import RETCODE
import logging

logger = logging.getLogger('blog')


class ArticleDetailView(View):
    """文章详情"""

    def get(self, request, article_id):

        try:
            # 获取本条数据
            article = Article.objects.get(id=article_id)
            # 获取上一条数据和下一条数据
            next_article = Article.objects.filter(id__gt=article.id, category2=article.category2).only('id', 'title').first()
            pre_article = Article.objects.filter(id__lt=article.id, category2=article.category2).only('id', 'title').order_by('-id').first()
            # 相关数据10条
            articles = Article.objects.filter(category2=article.category2).only('id', 'title')[0:9]
        except Exception as e:
            return http.HttpResponse('获取文章失败')

        # 阅读次数+1
        article.read_count += 1
        article.save()

        exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
                'markdown.extensions.toc']

        # 将markdown语法渲染成html样式
        article.content = markdown.markdown(article.content, extensions=exts)

        context = {
            'article': article,
            'next_article': next_article,
            'pre_article': pre_article,
            'articles': articles
        }

        return render(request, 'info.html', context=context)


class ArticleTopView(View):
    """点击排行"""

    def get(self, request):

        try:
            articles = Article.objects.order_by('-read_count').all().only('id', 'title')[0:7]
        except Exception as e:
            return http.HttpResponse('数据库错误')

        top_list = [{'title': article.title, 'id': article.id} for article in articles]

        return http.JsonResponse({'code': RETCODE.OK, 'top_list': top_list})


class RecommendView(View):
    """站长推荐"""

    def get(self, request):

        try:
            articles = Article.objects.filter(is_top=True).only('id', 'title', 'index_image')[0:6]
        except Exception as e:
            return http.HttpResponse('数据库错误')

        recommend_list = [{'title': article.title, 'id': article.id, 'index_image': article.index_image} for article in
                          articles]

        return http.JsonResponse({'code': RETCODE.OK, 'recommend_list': recommend_list})


class ArticleCountView(View):
    """获取文章数量"""

    def get(self, request):

        conn = get_redis_connection('default')
        pv = conn.get('24_hours_pv')


        try:
            count = Article.objects.count()
        except Exception as e:
            return http.HttpResponse('数据库错误')

        return http.JsonResponse({'code': RETCODE.OK, 'article_count': count, 'pv': int(pv)})


class AllArticleView(View):
    """所有文章"""

    def get(self, request, page_num):

        try:
            articles = Article.objects.order_by('-create_time').all().only('id', 'title')
            all_counts = articles.count()
        except Exception as e:
            return http.HttpResponse('数据库错误')

        # 分页
        paginator = Paginator(articles, constants.ARTICLE_LIST_LIMIT)
        try:
            page_articles = paginator.page(page_num)
        except EmptyPage:
            return http.HttpResponseNotFound('empty page')
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
            category = ArticleCategory.objects.get(id=category_id)
        except Exception as e:
            return http.HttpResponse('数据库错误')
        # 判断是否为一级分类
        if category.parent is None:
            articles = Article.objects.filter(category1=category)
            category_article_count = articles.count()
            # 分页
            paginator = Paginator(articles, constants.ARTICLE_LIST_LIMIT)
            try:
                page_articles = paginator.page(page_num)
            except EmptyPage:
                return http.HttpResponseNotFound('empty page')
            # 获取列表页总页数
            total_page = paginator.num_pages
            page_list = [i for i in range(total_page)]

            data_dict = {
                'category_id': category.id,
                'articles': page_articles,
                'category': category.name,
                'article_count': category_article_count,
                'total_page': page_list
            }
            # cat2_list = ArticleCategory.objects.filter(parent__isnull=False)

            # data_dict['categories'] = []
            #
            # for cat2 in cat2_list:
            #     data_dict['categories'].append({
            #         'id': cat2.id,
            #         'name': cat2.name
            #     })
            # data_dict['articles'] = page_articles
            #
            # data_dict['category'] = category.name
            # data_dict['count'] = category_article_count

        else:
            # 为二级分类
            articles = Article.objects.filter(category2=category)
            category_article_count = articles.count()

            # 分页
            paginator = Paginator(articles, constants.ARTICLE_LIST_LIMIT)
            try:
                page_articles = paginator.page(page_num)
            except EmptyPage:
                return http.HttpResponseNotFound('empty page')
            # 获取列表页总页数
            total_page = paginator.num_pages
            page_list = [i for i in range(total_page)]

            # cat2_list = ArticleCategory.objects.filter(parent__isnull=False)
            #
            # category2_list = []
            #
            # for cat2 in cat2_list:
            #     category2_list.append({
            #         'id': cat2.id,
            #         'name': cat2.name
            #     })
            # data_dict['articles'] = articles
            #
            # data_dict['category'] = category.name

            data_dict = {
                'category_id': category.id,
                'category': category.name,
                # 'categories': category2_list,
                'articles': page_articles,
                'article_count': category_article_count,
                'total_page': page_list
            }

        context = {'data': data_dict}

        return render(request, 'list2_1.html', context=context)


class LabelView(View):
    """获取标签"""

    def get(self, request):

        try:
            cat2_list = ArticleCategory.objects.filter(parent__isnull=False)

        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '获取标签失败'})

        # labels = [{'id': cat2.id, 'name': cat2.name} for cat2 in cat2_list]
        labels = []

        for cat2 in cat2_list:
            labels.append({
                'id': cat2.id,
                'name': cat2.name,
                'article_count': Article.objects.filter(category2=cat2).count()
            })

        return http.JsonResponse({'code': RETCODE.OK, 'labels': labels})


class ArticleLikeView(View):
    """文章点赞"""

    def get(self, request, article_id):

        try:
            article = Article.objects.get(id=article_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '获取失败'})

        # 获取请求的ip，一个ip只能点赞一次
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
        else:
            ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP

        redis = get_redis_connection('default')
        key = 'like_{}_flag_{}'.format(article_id, ip)
        if redis.get(key):
            return http.JsonResponse({'code': RETCODE.ALLOWERR, 'errmsg': '只能点击一次'})

        redis.set(key, 1, 600)

        article.like_count += 1
        article.save()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})
