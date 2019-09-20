from django.conf.urls import url

from article import views

urlpatterns = [
    url(r'article/detail/(?P<article_id>\d+)/$', views.ArticleDetailView.as_view(), name='article_detail')
]