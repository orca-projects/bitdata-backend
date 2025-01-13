from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils.response_helper import ResponseHelper

from applications.users.services import UserServices
from applications.binance_api.services import BinanceApiServices


class Collect(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = UserServices.get_kakao_id(user_info)
            binance_api_key = UserServices.get_binance_api_key(kakao_id)

            uid = BinanceApiServices.get_uid(binance_api_key)
            BinanceApiServices.save_uid(kakao_id, uid)

            # history = BinanceApiServices.get_history(binance_api_key)
            # BinanceApiServices.save_history(history)
        except Exception as e:
            return ResponseHelper.error(
                request=request,
                message="An error occurred",
                error_details=str(e),
            )

        return ResponseHelper.success(request=request)
