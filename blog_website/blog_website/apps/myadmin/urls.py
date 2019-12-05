from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from myadmin.views import users
from myadmin.views.users import AdminUserView


urlpatterns = [
    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),
]

router = DefaultRouter()
router.register('users', AdminUserView, base_name='users')
urlpatterns += router.urls