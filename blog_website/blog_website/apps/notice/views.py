from django import http
from django.shortcuts import render


# Create your views here.
from django.views import View

from blog_website.response_code import RETCODE
from notice.models import Notice


class NoticeView(View):
    """获取公告"""
    def get(self, request):

        try:
            notices = Notice.objects.all()
        except Exception as e:
            return http.HttpResponse('数据库查询错误')

        notice_list = []
        for notice in notices:
            if notice.is_up is True:
                notice_list.insert(0, {'title': notice.title})
            else:
                notice_list.append({'title': notice.title})
        return http.JsonResponse({"code": RETCODE.OK, "notice_list": notice_list})

def test(request):
    return render(request, 'index.html')