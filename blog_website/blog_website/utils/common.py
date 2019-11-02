import datetime
import ssl
import urllib
from PIL import Image
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404


def get_image_size(url):
    context = ssl._create_unverified_context()
    img = Image.open(urllib.request.urlopen(url, context=context))
    l, w  = img.size
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
    paginator = Paginator(query_set,page_size)
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
