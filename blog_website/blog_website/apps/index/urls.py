from django.conf.urls import url

from index import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index_list')
]