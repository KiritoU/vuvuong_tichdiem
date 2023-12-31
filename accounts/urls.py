from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views

urlpatterns = [
    path("history/", views.UserHistoryListAPIView.as_view(), name="history"),
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("info/", views.UserInfoView.as_view(), name="user_infor"),
    path("checkin/", views.UserCheckinAPIView.as_view(), name="user_checkin"),
    # path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    # path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
]
