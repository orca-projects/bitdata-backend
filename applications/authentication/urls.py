from django.urls import path
from applications.authentication.views import (
    KakaoLogin,
    KakaoLoginCallback,
    Join,
    LogoutView,
    MeView,
)

urlpatterns = [
    path("login/kakao/", KakaoLogin.as_view(), name="login-kakao"),
    path(
        "login/kakao/callback/",
        KakaoLoginCallback.as_view(),
        name="login-kakao-callback",
    ),
    path("join/", Join.as_view(), name="join"),
    path("logout/", LogoutView.as_view(), name="logout"), # 로그아웃 엔드포인트 추가
    path("me/", MeView.as_view(), name="me"), # 로그인 사용자 정보 조회 엔드포인트 추가
]
