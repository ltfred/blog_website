from django.conf.urls import url

from user import views

urlpatterns = [
    # 关于我
    url(r'^about/$', views.AboutUserView.as_view(), name='about'),
]