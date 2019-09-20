from django.conf.urls import url

from notice import views

urlpatterns = [
    # 所有公告
    url(r'^notices/$', views.NoticeView.as_view(), name='notice'),
    # 公告详情
    url(r'^notice/detail/(?P<notice_id>\d+)/$', views.NoticeDetailView.as_view())
]
