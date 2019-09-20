from django.conf.urls import url

from article import views

urlpatterns = [
    # 文章详情
    url(r'article/detail/(?P<article_id>\d+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    # 热点排行
    url(r'top/$', views.ArticleTopView.as_view(), name='top_list'),
    # 文章推荐
    url(r'recommend/$', views.RecommendView.as_view(), name='recommend_list'),
    # 文章总数统计
    url(r'article/count/$', views.ArticleCountView.as_view(), name='article_count'),
    # 所有文章
    url(r'articles/$', views.AllArticleView.as_view(), name='articles'),
]