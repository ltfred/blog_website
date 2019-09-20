from django.conf.urls import url

from user import views

urlpatterns = [
    url(r'^profile/$', views.UserProfileView.as_view(), name='profile'),
    url(r'about/$', views.AboutUserView.as_view(), name='about'),
]