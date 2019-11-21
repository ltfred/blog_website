import datetime
import ssl
import time
import urllib
from PIL import Image
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django_redis import get_redis_connection

from article.models import ArticleCategory, Article, Label
from notice.models import Notice
from photo.models import PhotoCategory


def get_image_size(url):
    context = ssl._create_unverified_context()
    img = Image.open(urllib.request.urlopen(url, context=context))
    l, w = img.size
    return str(l) + '×' + str(w)


def get_ip(request):
    # 获取请求的ip
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')  # 判断是否使用代理
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 使用代理获取真实的ip
    else:
        ip = request.META.get('REMOTE_ADDR')  # 未使用代理获取IP
    return ip


def paginator_function(query_set, page_num, page_size):
    # 分页
    paginator = Paginator(query_set, page_size)
    try:
        page_query_set = paginator.page(page_num)
    except EmptyPage:
        raise Http404
    # 获取列表页总页数
    total_page = paginator.num_pages
    return page_query_set, total_page


def str2datetime(m_str):
    return datetime.datetime.strptime(m_str, '%Y-%m-%d')


def datetime2str(m_datetime):
    return m_datetime.strftime("%Y-%m-%d")


def get_photo_category():
    photo_category_query_set = PhotoCategory.objects.all()

    photo_categories = [{'id': photo_category.id, 'name': photo_category.name} for photo_category in
                        photo_category_query_set]

    return photo_categories


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


def get_article_count():
    count = Article.objects.count()
    return count


def get_notice():
    try:
        notices = Notice.objects.all().only('id', 'title').order_by('-create_time')[0:8]
    except:
        raise Http404
    notice_list = []
    for notice in notices:
        if notice.is_up is True:
            notice_list.insert(0, {'title': notice.title, 'id': notice.id})
        else:
            notice_list.append({'title': notice.title, 'id': notice.id})
    return notice_list


def get_recommend():
    try:
        articles = Article.objects.filter(is_top=True).only('id', 'title', 'index_image')[0:6]
    except Exception as e:
        raise Http404
    recommend_list = [{'title': article.title, 'id': article.id, 'index_image': article.index_image} for article in
                      articles]
    return recommend_list


def get_top():
    try:
        articles = Article.objects.order_by('-read_count').all().only('id', 'title')[0:7]
    except Exception as e:
        raise Http404
    top_list = [{'title': article.title, 'id': article.id} for article in articles]
    return top_list


def get_labels():
    try:
        # 获取所有标签
        labels_queryset = Label.objects.all()
    except Exception as e:
       raise Http404
    labels = []
    for label in labels_queryset:
        labels.append({
            'id': label.id,
            'name': label.name,
            'article_count': label.article_set.all().count()  # 每个标签下的文章的数量
        })
    return labels


def get_site_info():
    conn = get_redis_connection('default')
    pv = conn.get('24_hours_pv')
    now_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    now_time = str2datetime(now_time)
    begin_time = str2datetime('2019-08-29')
    days = (now_time - begin_time).days

    try:
        count = get_article_count()
    except Exception as e:
        raise Http404
    return count, int(pv), days
