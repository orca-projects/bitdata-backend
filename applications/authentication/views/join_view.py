from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils.response_helper import ResponseHelper

from applications.authentication.services import JoinService
from applications.users.repositories import UserRepository


class Join(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_data = JoinService.get_user_data(request)

            UserRepository.set_user(user_data)
        except ValueError as ve:
            print(ve)
            return ResponseHelper.error(message="ValueError")
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(message="로그인 성공")
