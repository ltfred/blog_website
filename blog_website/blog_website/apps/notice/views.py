from django import http
from django.shortcuts import render


# Create your views here.
from django.views import View

from blog_website.response_code import RETCODE
from notice.models import Notice


class NoticeView(View):
    """获取所有公告"""
    def get(self, request):

        try:
            notices = Notice.objects.all()
        except Exception as e:
            return http.HttpResponse('数据库查询错误')

        notice_list = []
        for notice in notices:
            if notice.is_up is True:
                notice_list.insert(0, {'title': notice.title, 'id': notice_list.id})
            else:
                notice_list.append({'title': notice.title, 'id': notice.id})
        return http.JsonResponse({"code": RETCODE.OK, "notice_list": notice_list})


class NoticeDetailView(View):
    """公告详情"""
    def get(self, request, notice_id):

        try:
            notice = Notice.objects.get(id=notice_id)
        except:
            return http.HttpResponse('查询失败')
        context = {'notice': notice}

        return render(request, 'info.html', context=context)


def test(request):
    return render(request, 'index.html')