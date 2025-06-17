from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from rest_framework.views import APIView

from core.utils.response_util import ResponseUtil
from applications.authentication.services import KakaoService, AuthenticationService
from applications.authentication.utils import StateUtil
from applications.users.services import UserService, UserApiKeyService


class KakaoLogin(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request) -> JsonResponse:
        state = StateUtil.get_sate()
        request.session["oauth_state"] = state

        login_url = KakaoService.get_login_url(state)

        return ResponseUtil.success(data={"login_url": login_url})


class KakaoLoginCallback(APIView):
    def post(self, request) -> JsonResponse:
        try:
            KakaoService.check_sate(request)

            access_token = KakaoService.get_access_token(request)

            user_data = KakaoService.fetch_user_data(access_token)

            request.session["user_data"] = user_data

            kakao_uid = user_data["kakao_uid"]
            is_member = UserService.is_member(kakao_uid)
            has_binance_key = UserApiKeyService.has_binance_api_key(kakao_uid)

            AuthenticationService.kakao_authenticated(request)

            if is_member:
                AuthenticationService.login(request, kakao_uid)

            request.session["has_api_key"] = has_binance_key

            return ResponseUtil.success(
                data={
                    "is_member": is_member,
                    "has_binance_key": has_binance_key,
                },
            )

        except Exception as e:
            print(e)
            return ResponseUtil.error()
        
class NextStepView(APIView):
    def get(self, request) -> JsonResponse:
        is_member = request.session.get("is_login", False)
        has_api_key = request.session.get("has_api_key", False)

        referer = request.META.get("HTTP_REFERER", "")
        came_from_join = referer.endswith("/join")

        if not is_member:
            return ResponseUtil.success(data={"next_step": "join"})

        if came_from_join:
            return ResponseUtil.success(data={"next_step": "onboarding"})

        if not has_api_key:
            return ResponseUtil.success(data={"next_step": "setting"})

        return ResponseUtil.success(data={"next_step": "collect"})
