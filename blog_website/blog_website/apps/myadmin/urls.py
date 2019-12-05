from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from myadmin.views import users, statistical
from myadmin.views.users import AdminUserView


urlpatterns = [
    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),
    url(r'^statistical/user_count/$', statistical.AdminUserCount.as_view()),
    url(r'^statistical/article_count/$', statistical.AdminArticleCount.as_view()),
    url(r'^statistical/photo_count/$', statistical.AdminPhotoCount.as_view()),
    url(r'^statistical/label_count/$', statistical.AdminLabelCount.as_view()),
    url(r'^statistical/day_active/$', statistical.AdminUserDayActiveCount.as_view()),
    url(r'^statistical/month_increment/$', statistical.AdminArticleMonthCountView.as_view()),
    url(r'^statistical/label_article/$',statistical.AdminLabelArticle.as_view()),
]

router = DefaultRouter()
router.register('users', AdminUserView, base_name='users')
urlpatterns += router.urls