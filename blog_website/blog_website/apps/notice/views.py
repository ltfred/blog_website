from django import http
from django.http import Http404
from django.shortcuts import render
from django.views import View
from blog_website.utils.response_code import RETCODE
from notice.models import Notice
import logging
logger = logging.getLogger('blog')


class NoticeView(View):
    """获取前8条公告"""

    def get(self, request):

        try:
            notices = Notice.objects.all().only('id', 'title').order_by('-create_time')[0:8]
        except Exception as e:
            logger.error(e)
            # return http.HttpResponse('数据库查询错误')
            raise Http404
        notice_list = []
        for notice in notices:
            if notice.is_up is True:
                notice_list.insert(0, {'title': notice.title, 'id': notice.id})
            else:
                notice_list.append({'title': notice.title, 'id': notice.id})
        return http.JsonResponse({"code": RETCODE.OK, "notice_list": notice_list})


class NoticeDetailView(View):
    """公告详情"""

    def get(self, request, notice_id):

        try:
            # 获取本条数据
            notice = Notice.objects.get(id=notice_id)
            # 获取上一条数据和下一条数据
            next_notice = Notice.objects.filter(id__gt=notice.id).first()
            pre_notice = Notice.objects.filter(id__lt=notice.id).order_by('-id').first()
            # 相关数据10条
            notices = Notice.objects.all()[0:9]
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库错误'})

        # 每访问一次此页面阅读数+1
        notice.read_count += 1
        notice.save()

        context = {
            'notice': notice,
            'next_notice': next_notice,
            'pre_notice': pre_notice,
            'notices': notices
        }

        return render(request, 'notice_detail.html', context=context)


class NoticeLikeView(View):
    """公告点赞"""
    def get(self, request, notice_id):

        try:
            notice = Notice.objects.get(id=notice_id)
        except Exception as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '获取失败'})
        # 阅读数 + 1
        notice.like_count += 1
        notice.save()

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'ok'})


class AllNoticeView(View):
    """所有公告"""
    def get(self, request):
        try:
            notices = Notice.objects.all()
        except Exception as e:
            logger.error(e)
            # return http.HttpResponse('服务器出错了')
            raise Http404
        context = {'notices': notices}
        return render(request, 'notice_list.html', context=context)
