from django.conf.urls import url

from comment import views

urlpatterns = [
    url(r'^comment/$', views.CommentView.as_view(), name='list'),
]