from django.urls import path
from auths.views import GetKakaoLoginUrl, KakaoLoginCallback, ConsentView, SaveBinanceKeys
from . import views

# from auths.views import 

urlpatterns = [
    path('login/kakao/', GetKakaoLoginUrl.as_view(), name='kakao-login-initiate'),
    path('login/kakao/callback/', KakaoLoginCallback.as_view(), name='kakao-login-callback'),
    path('login/kakao/consent/', ConsentView.as_view(), name='kakao-login-consent'),
    path('login/get/csrf/', views.get_csrf_token),
    path('onboarding/keys/save/', SaveBinanceKeys.as_view(), name='onboarding-binance-key-save'),
]