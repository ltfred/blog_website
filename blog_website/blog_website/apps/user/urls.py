from django.conf.urls import url
from user import views

urlpatterns = [
    # 关于我
    url(r'^about/$', views.AboutUserView.as_view(), name='about'),
    url(r'^music/$', views.MusicView.as_view(), name='music'),
    url(r'^login/$', views.LoginView.as_view(), name='login'),
]