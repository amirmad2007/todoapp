from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import *

urlpatterns = [
    path("jwt/create/", CustomTokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt_verify"),
    path("token/login/", CustomObtainToken.as_view(), name="login-token"),
    path("token/logout/", DelteAuthTokenApiView.as_view(), name="login-login"),
    path("profile/", ProfileApiView.as_view(), name="profile"),
    path("register/", RegisterApiView.as_view(), name="register_user"),
    path("change-password/", ChangePasswordApiView.as_view(), name="change-password"),
    path(
        "email-verification/<str:token>",
        VerifyApiView.as_view(),
        name="email-verification",
    ),
    path(
        "email-verification/resend/",
        ResendVerificationApiView.as_view(),
        name="resend_verification",
    ),
    path(
        "request-to-rest-password/",
        RequestResetPasswordApiView.as_view(),
        name="request_to_rest_password",
    ),
    path(
        "reset-password/<str:token>",
        ResendPasswordApiView.as_view(),
        name="reset_password",
    ),
]
