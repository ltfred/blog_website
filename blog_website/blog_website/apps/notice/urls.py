from django.conf.urls import url

from notice import views

urlpatterns = [
    # 所有公告
    url(r'^notices/$', views.NoticeView.as_view(), name='notice'),
    # 公告详情
    url(r'^notice/detail/(?P<notice_id>\d+)/$', views.NoticeDetailView.as_view(), name='notice_detail'),
    # 公告点赞
    url(r'notice/like/(?P<notice_id>\d+)/$', views.NoticeLikeView.as_view(), name='notice_like'),
]
