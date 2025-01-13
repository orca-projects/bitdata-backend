from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils.response_helper import ResponseHelper

from applications.authentication.services import JoinServices


class Join(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_info = JoinServices.get_user_info(request)

            JoinServices.save_user_info(user_info)
        except ValueError as ve:
            return ResponseHelper.error(request=request, message=str(ve))
        except Exception as e:
            return ResponseHelper.error(
                request=request,
                message="An error occurred",
                error_details=str(e),
            )

        return ResponseHelper.success(request=request)
