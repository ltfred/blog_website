from django.conf.urls import url

from user import views

urlpatterns = [
    # 首页个人信息
    url(r'^profile/$', views.UserProfileView.as_view(), name='profile'),
    # 关于我
    url(r'about/$', views.AboutUserView.as_view(), name='about'),
]