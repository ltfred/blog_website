import datetime
import ssl
import urllib
from PIL import Image
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404

from article.models import ArticleCategory
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