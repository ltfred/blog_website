from django.conf.urls import url

from notice import views

urlpatterns = [
    url(r'^test/$', views.test),
    url(r'^notice/$', views.NoticeView.as_view(), name='notice'),
    url(r'^test/notice/detail/(?P<notice_id>\d+)/$', views.NoticeDetailView.as_view())
]
