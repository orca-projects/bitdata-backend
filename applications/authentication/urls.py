from django.urls import path
from applications.authentication.views import (
    LoginState,
    KakaoLogin,
    KakaoLoginCallback,
    Join,
    Logout,
)

urlpatterns = [
    path("login/state/", LoginState.as_view(), name="login-state"),
    path("login/kakao/", KakaoLogin.as_view(), name="login-kakao"),
    path(
        "login/kakao/callback/",
        KakaoLoginCallback.as_view(),
        name="login-kakao-callback",
    ),
    path("join/", Join.as_view(), name="join"),
    path("logout/", Logout.as_view(), name="logout"),
]
