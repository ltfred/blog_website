from django import http
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from article.models import ArticleCategory
from blog_website.utils.common import get_photo_category, get_notice, get_recommend, get_top, get_labels
from blog_website.utils.responseCode import RETCODE
from notice.models import Notice
import logging

logger = logging.getLogger('blog')


class NoticeView(View):
    """获取前8条公告"""

    def get(self, request):
        notice_list = get_notice()
        return http.JsonResponse({"code": RETCODE.OK, "notice_list": notice_list})


class NoticeDetailView(View):
    """公告详情"""

    def get(self, request, notice_id):
        try:
            notice = Notice.objects.get(id=notice_id)
            next_notice = Notice.objects.filter(id__gt=notice.id).first()
            pre_notice = Notice.objects.filter(id__lt=notice.id).order_by('-id').first()
            notices = Notice.objects.exclude(id=notice.id)[0:9]
        except Exception as e:
            logger.error(e)
            raise
        # 每访问一次此页面阅读数+1
        notice.read_count += 1
        notice.save()

        context = {
            'notice': notice,
            'next_notice': next_notice,
            'pre_notice': pre_notice,
            'notices': notices,
            'cat_list': ArticleCategory.get_cat_lst(),
            'photo_category': get_photo_category(),
            'recommend_list': get_recommend(),
            'top_list': get_top(),
            'labels': get_labels(),
        }
        return render(request, 'noticeDetail.html', context=context)


class NoticeLikeView(View):
    """公告点赞"""

    def post(self, request, notice_id):
        try:
            notice = Notice.objects.get(id=notice_id)
        except Exception as e:
            logger.error(e)
            raise
        notice.like_count += 1
        notice.save()
        return http.HttpResponse('success')


class AllNoticeView(TemplateView):
    template_name = 'noticeList.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        notices = Notice.objects.all()
        context['notices'] = notices
        context['cat_list'] = ArticleCategory.get_cat_lst()
        context['photo_category'] = get_photo_category()
        context['recommend_list'] = get_recommend()
        context['top_list'] = get_top()
        context['labels'] = get_labels()
        return context
