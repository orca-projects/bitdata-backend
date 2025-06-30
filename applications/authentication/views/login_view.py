from django.http import JsonResponse
from rest_framework.views import APIView
from core.utils.response_util import ResponseUtil
from applications.users.services import ProfileService

class LoginState(APIView):
    def get(self, request) -> JsonResponse:
        is_login = request.session.get("is_login", False)
        is_connected = False

        if is_login:
            user_data = request.session.get("user_data", {})
            kakao_uid = user_data.get("kakao_uid")
            if kakao_uid:
                profile = ProfileService.get_profile(kakao_uid)
                if profile:
                    is_connected = profile.get("is_connected", False)

        return ResponseUtil.success(data={
            "is_login": is_login,
            "is_connected": is_connected,
        })
