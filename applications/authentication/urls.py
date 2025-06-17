from django.urls import path
from applications.authentication.views import (
    KakaoLogin,
    KakaoLoginCallback,
    Join,
    Logout,
    NextStepView,
)

urlpatterns = [
    path("login/kakao/", KakaoLogin.as_view(), name="login-kakao"),
    path(
        "login/kakao/callback/",
        KakaoLoginCallback.as_view(),
        name="login-kakao-callback",
    ),
    path("join/", Join.as_view(), name="join"),
    path("logout/", Logout.as_view(), name="logout"),
    path("next-step/", NextStepView.as_view(), name="next-step"), 
]
