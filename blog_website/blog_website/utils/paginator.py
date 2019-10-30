from django.core.paginator import Paginator, EmptyPage
from django.http import Http404


def paginator_function(query_set, page_num, page_size):
    # 分页
    paginator = Paginator(query_set,page_size)
    try:
        page_query_set = paginator.page(page_num)
    except EmptyPage:
        # return http.HttpResponseNotFound('empty page')
        raise Http404
    # 获取列表页总页数
    total_page = paginator.num_pages
    return page_query_set, total_page
