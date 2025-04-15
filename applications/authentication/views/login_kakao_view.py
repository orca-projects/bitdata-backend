from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from core.utils.response_helper import ResponseHelper

from applications.authentication.services import KakaoService
from applications.authentication.utils import StateUtil
from applications.users.services import UserService, UserApiKeyService


class KakaoLogin(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request) -> JsonResponse:
        state = StateUtil.get_sate()
        request.session["oauth_state"] = state

        login_url = KakaoService.get_login_url(state)

        return ResponseHelper.success(data={"login_url": login_url})


class KakaoLoginCallback(APIView):
    def post(self, request) -> JsonResponse:
        session_state = request.session.get("oauth_state")
        code = request.data.get("code")
        request_state = request.data.get("state")

        try:
            KakaoService.validate_sate(session_state, request_state)

            access_token = KakaoService.get_access_token(code)
            KakaoService.validate_access_token(access_token)

            user_data = KakaoService.get_user_data(access_token)
            KakaoService.validate_user_data(user_data)

            KakaoService.save_session_user_data(request, user_data)

            kakao_uid = user_data["kakao_uid"]
            is_member = UserService.is_member(kakao_uid)
            has_binance_key = UserApiKeyService.has_binance_api_key(kakao_uid)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "is_member": is_member,
                "has_binance_key": has_binance_key,
            },
        )
