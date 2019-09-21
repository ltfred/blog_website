from django.conf.urls import url

from photo import views

urlpatterns = [

    # 照片分类
    url(r'^photo/categories/$', views.PhotoCategoryView.as_view(), name='photo_categories'),
    # 所有照片
    url(r'^photos/$', views.AllPhotosView.as_view(), name='photos'),
    # 该类别下所有照片
    url(r'^photos/(?P<category_id>\d+)/$', views.CategoryPhotoView.as_view(), name='photo_category'),

]