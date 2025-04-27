from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils.response_util import ResponseUtil

from applications.users.repositories import UserRepository


class Join(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_data = request.session.get("user_data")

            UserRepository.set_user(user_data)
        except ValueError as ve:
            print(ve)
            return ResponseUtil.error(message="ValueError")
        except Exception as e:
            print(e)
            return ResponseUtil.error()

        return ResponseUtil.success(message="join success")
