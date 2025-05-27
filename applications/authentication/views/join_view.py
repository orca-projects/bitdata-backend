from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils.response_util import ResponseUtil
from applications.authentication.services import AuthenticationService
from applications.users.services import UserService


class Join(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_data = request.session.get("user_data")

            UserService.join(user_data)

            kakao_uid = user_data["kakao_uid"]

            AuthenticationService.login(request, kakao_uid)

            return ResponseUtil.success(message="join success")
        except ValueError as ve:
            print(ve)
            return ResponseUtil.error(message="ValueError")
        except Exception as e:
            print(e)
            return ResponseUtil.error()
