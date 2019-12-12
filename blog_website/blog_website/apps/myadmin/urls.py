from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from myadmin.views import users, statistical, article, photo
from myadmin.views.article import AdminArticleView, AdminArticleLabelView, AdminCarouselView
from myadmin.views.link import AdminLinkView
from myadmin.views.photo import AdminPhotoCategoryView, AdminPhotoView
from myadmin.views.soup import AdminSoupView
from myadmin.views.users import AdminUserView

urlpatterns = [
    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),
    url(r'^statistical/user_count/$', statistical.AdminUserCount.as_view()),
    url(r'^statistical/article_count/$', statistical.AdminArticleCount.as_view()),
    url(r'^statistical/photo_count/$', statistical.AdminPhotoCount.as_view()),
    url(r'^statistical/label_count/$', statistical.AdminLabelCount.as_view()),
    url(r'^statistical/day_active/$', statistical.AdminUserDayActiveCount.as_view()),
    url(r'^statistical/month_increment/$', statistical.AdminArticleMonthCountView.as_view()),
    url(r'^statistical/label_article/$', statistical.AdminLabelArticle.as_view()),
    url(r'^articles/simple/$', article.AdminArticleSimpleView.as_view()),
    url(r'^author/simple/$', article.AdminAuthorSimpleView.as_view()),
    url(r'^articles/categories/$', article.AdminArticleCategory1View.as_view()),
    url(r'^articles/categories/(?P<category_id>\d+)/$', article.AdminArticleCategory2View.as_view()),
    url(r'^labels/simple/$', article.AdminLabelView.as_view()),
    url(r'^article/index_image/$', article.AdminArticleIndexImageView.as_view()),
    url(r'^article/categories/simple$', article.AdminArticleCategorySimpleView.as_view()),
    url(r'^article/categories/(?P<category_id>\d+)/$', article.AdminArticleCategoryUpdateView.as_view()),
    url(r'^article/categories/$', article.AdminArticleCategory.as_view()),
    url(r'^article/category/image/$', article.AdminCategoryImageView.as_view()),
    url(r'^photos/categories/$', photo.AdminPhotoCategory.as_view()),
    url(r'^photos/image/$', photo.AdminPhotoImageView.as_view()),
    url(r'^photos/simple/$', photo.AdminPhotosSimpleView.as_view()),
]

router = DefaultRouter()
router.register('users', AdminUserView, base_name='users')
urlpatterns += router.urls

router = DefaultRouter()
router.register('articles', AdminArticleView, base_name='articles')
urlpatterns += router.urls

router = DefaultRouter()
router.register('link', AdminLinkView, base_name='link')
urlpatterns += router.urls

router = DefaultRouter()
router.register('photo/categories', AdminPhotoCategoryView, base_name='photo_category')
urlpatterns += router.urls

router = DefaultRouter()
router.register('photos', AdminPhotoView, base_name='photos')
urlpatterns += router.urls

router = DefaultRouter()
router.register('labels', AdminArticleLabelView, base_name='labels')
urlpatterns += router.urls

router = DefaultRouter()
router.register('carousel', AdminCarouselView, base_name='carousel')
urlpatterns += router.urls

router = DefaultRouter()
router.register('soup', AdminSoupView, base_name='soup')
urlpatterns += router.urls