from django.conf.urls import url
from index import views

urlpatterns = [
    # 首页
    url(r'^$', views.IndexView.as_view(), name='index_list'),
    # 首页分类
    url(r'^category/$', views.CategoryView.as_view(), name='category'),
]