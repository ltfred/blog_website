from django.conf.urls import url

from article import views, feed

urlpatterns = [
    # 文章详情
    url(r'^article/detail/(?P<article_id>\d+)/$', views.ArticleDetailView.as_view(), name='article_detail'),
    # 热点排行
    url(r'^top/$', views.ArticleTopView.as_view(), name='top_list'),
    # 文章推荐
    url(r'^recommend/$', views.RecommendView.as_view(), name='recommend_list'),
    # 文章总数统计
    url(r'^article/count/$', views.ArticleCountView.as_view(), name='article_count'),
    # 所有文章
    url(r'^articles/(?P<page_num>\d+)/$', views.AllArticleView.as_view(), name='article'),
    # 该类别下的所有文章
    url(r'^list/(?P<category_id>\d+)/(?P<page_num>\d+)/$', views.CategoryAllArticleView.as_view(), name='category_list'),
    # 获取标签
    url(r'^labels/$', views.LabelView.as_view(), name='labels'),
    # 文章点赞
    url(r'article/like/(?P<article_id>\d+)/$', views.ArticleLikeView.as_view(), name='article_like'),
    # 获取该标签下的所有文章
    url(r'^label/articles/(?P<label_id>\d+)/(?P<page_num>\d+)/$', views.LabelArticlesView.as_view(), name='label_articles'),

    url(r'search/', views.ArticleSearchView()),
    url('rss/', feed.BlogFeed(), name='rss'),
]
