from collections import OrderedDict
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultPagination(PageNumberPagination):
    """自定义分页类"""
    # 指定分页默认页容量
    page_size = 5
    # 指定获取分页数据时指定`页容量`的参数名称
    page_size_query_param = 'pagesize'
    # 指定分页最大页容量
    max_page_size = 20

    def get_paginated_response(self, data):
        """重写父类方法，自定义分页响应数据格式"""
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('lists', data),
            ('page', self.page.number),
            ('pages', self.page.paginator.num_pages),
            ('pagesize', self.get_page_size(self.request))
        ]))