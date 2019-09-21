from django.conf.urls import url

from links import views

urlpatterns = [
    url(r'links/$', views.LinkView.as_view(), name='list'),
]