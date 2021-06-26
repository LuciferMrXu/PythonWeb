# jwt内部实现的登陆视图
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
from django.urls import path, include
from apps.users.views import UserViewSet,LoginView,UserControlViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'user', UserControlViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path(r"user/login", obtain_jwt_token),
    path(r"user/info", LoginView.userInfo),
    path(r"user/logout", LoginView.userLogout),
    path(r"user/resetToken", refresh_jwt_token),
]

