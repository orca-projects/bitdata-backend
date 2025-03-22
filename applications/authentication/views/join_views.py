from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils.response_helper import ResponseHelper

from applications.authentication.services import JoinServices
from applications.users.repositories import UserRepository


class Join(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_info = JoinServices.get_user_info(request)

            UserRepository.create(user_info)
        except ValueError as ve:
            print(ve)
            return ResponseHelper.error(message="ValueError")
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(message="로그인 성공")
