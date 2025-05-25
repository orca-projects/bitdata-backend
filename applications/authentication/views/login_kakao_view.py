from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from core.utils.response_util import ResponseUtil

from applications.authentication.services import KakaoService
from applications.authentication.utils import StateUtil
from applications.users.services import UserService, UserApiKeyService
from django.contrib.auth import logout  # 로그아웃 처리를 위해 추가
from rest_framework.permissions import IsAuthenticated  # 인증된 사용자만 접근 가능하도록
from rest_framework.permissions import AllowAny


class KakaoLogin(APIView):
    permission_classes = [AllowAny]
    @method_decorator(ensure_csrf_cookie)
    def get(self, request) -> JsonResponse:
        state = StateUtil.get_sate()
        request.session["oauth_state"] = state

        login_url = KakaoService.get_login_url(state)

        return ResponseUtil.success(data={"login_url": login_url})


class KakaoLoginCallback(APIView):
    permission_classes = [AllowAny]
    def post(self, request) -> JsonResponse:
        try:
            KakaoService.check_sate(request)

            access_token = KakaoService.get_access_token(request)

            user_data = KakaoService.fetch_user_data(access_token)

            request.session["user_data"] = user_data

            kakao_uid = user_data["kakao_uid"]
            is_member = UserService.is_member(kakao_uid)
            has_binance_key = UserApiKeyService.has_binance_api_key(kakao_uid)
        except Exception as e:
            print(e)
            return ResponseUtil.error()

        return ResponseUtil.success(
            data={
                "is_member": is_member,
                "has_binance_key": has_binance_key,
            },
        )
    

# 로그아웃 API 뷰 추가
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def post(self, request):
        logout(request)  # Django 기본 세션 로그아웃 처리
        return ResponseUtil.success(message="로그아웃 완료")
    

# 로그인 사용자 정보 조회 API 뷰 추가
class MeView(APIView):
    permission_classes = [AllowAny]
    permission_classes = [IsAuthenticated]  # 로그인한 사용자만 접근 가능

    def get(self, request):
        user = request.user  # 현재 로그인한 사용자 정보 가져오기
        return ResponseUtil.success(data={
            "user_id": user.id,
            "name": user.name,
            "email": user.account_email,
            "phone": user.phone_number,
        })