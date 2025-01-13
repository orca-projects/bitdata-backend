from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils import ResponseHelper

from applications.users.services import UserServices


class BinanceKey(APIView):
    def post(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = UserServices.get_kakao_id(user_info)
            binance_api_key = {
                "api_key": request.data.get("api_key"),
                "secret_key": request.data.get("secret_key"),
            }

            UserServices.save_binance_key(kakao_id, binance_api_key)
        except Exception as e:
            return ResponseHelper.error(
                request=request,
                message="An error occurred",
                error_details=str(e),
            )

        return ResponseHelper.success(request=request)
