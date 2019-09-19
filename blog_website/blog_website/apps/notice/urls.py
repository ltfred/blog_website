from django.conf.urls import url

from notice import views

urlpatterns = [
    url(r'^notices/$', views.NoticeView.as_view(), name='notice'),
    url(r'^notice/detail/(?P<notice_id>\d+)/$', views.NoticeDetailView.as_view())
]
