from django.conf.urls import url

from article import views

urlpatterns = [
    url(r'article/detail/(?P<article_id>\d+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    url(r'top/$', views.ArticleTopView.as_view(), name='top_list'),
    url(r'recommend/$', views.RecommendView.as_view(), name='recommend_list'),
]