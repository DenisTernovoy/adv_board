from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views
from users.apps import UsersConfig

app_name = UsersConfig.name

urlpatterns = [
    path(
        "register/",
        views.CreateUser.as_view(permission_classes=(AllowAny,)),
        name="register",
    ),
    path(
        "login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="login",
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(permission_classes=(AllowAny,)),
        name="token_refresh",
    ),
    path(
        "reset_password/",
        views.UserResetPassword.as_view(permission_classes=(AllowAny,)),
        name="reset_password",
    ),
    path(
        "reset_password_confirm",
        views.UserResetPasswordConfirm.as_view(permission_classes=(AllowAny,)),
        name="reset_password_confirm",
    ),
]
