from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from core.utils.response_helper import ResponseHelper

from applications.authentication.services import KakaoServices
from applications.authentication.utils import StateHelper
from applications.users.services import UserServices


class KakaoLogin(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request) -> JsonResponse:
        state = StateHelper.get_sate()
        request.session["oauth_state"] = state

        login_url = KakaoServices.get_login_url(state)

        return ResponseHelper.success(data={"login_url": login_url})


class KakaoLoginCallback(APIView):
    def post(self, request) -> JsonResponse:
        session_state = request.session.get("oauth_state")
        code = request.data.get("code")
        request_state = request.data.get("state")

        try:
            KakaoServices.validate_sate(session_state, request_state)

            access_token = KakaoServices.get_access_token(code)
            KakaoServices.validate_access_token(access_token)

            user_info = KakaoServices.get_user_info(access_token)
            KakaoServices.validate_user_info(user_info)

            KakaoServices.save_session_user_info(request, user_info)

            kakao_id = user_info["kakao_id"]
            is_member = UserServices.is_member(kakao_id)
            has_binance_key = UserServices.has_binance_api_key(kakao_id)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "is_member": is_member,
                "has_binance_key": has_binance_key,
            },
        )
