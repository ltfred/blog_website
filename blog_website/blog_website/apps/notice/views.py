from django import http
from django.shortcuts import render
from django.views import View
from blog_website.utils.response_code import RETCODE
from notice.models import Notice
import logging
logger = logging.getLogger('blog')


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
        except Exception as e:
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库错误'})

        # 每访问一次此页面阅读数+1
        notice.read_count += 1
        notice.save()

        context = {'notice': notice}

        return render(request, 'notice_detail.html', context=context)


class NoticeLikeView(View):
    """文章点赞"""
    def get(self, request, notice_id):

        try:
            notice = Notice.objects.get(id=notice_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '获取失败'})

        notice.like_count += 1
        notice.save()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})