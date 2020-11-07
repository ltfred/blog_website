from django.conf.urls import url

from photo import views

urlpatterns = [

    # 照片分类
    url(r'^photo/categories/$', views.PhotoCategoryView.as_view(), name='photo_categories'),
    # 获取所有照片组
    url(r"^photo/groups/(?P<page_num>\d+)/$", views.PhotoGroupView.as_view(), name="all_groups"),
    # 获取某分类下所有照片组
    url(r"^photo/category/groups/(?P<category_id>\d+)/(?P<page_num>\d+)/$", views.CategoryPhotoGroupView.as_view(), name="category_group"),
    # 获取分组下的所有照片
    url(r"^photo/group/photos/(?P<group_id>\d+)/$", views.Photos.as_view(), name="photos"),

]