from django.http import JsonResponse
from rest_framework.views import APIView
from core.utils import ResponseHelper

from applications.users.services import (
    UserKeyInfoServices,
    ProfileServices,
)
from applications.transaction.services import (
    CollectServices,
    PositionCalculatorServices,
    TransactionServices,
)


class BinanceKey(APIView):
    def post(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = user_info["kakao_id"]
            binance_api_key = {
                "api_key": request.data.get("api_key"),
                "secret_key": request.data.get("secret_key"),
            }

            UserKeyInfoServices.save_binance_api_key(kakao_id, binance_api_key)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success()


class Collect(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_connected = True
        self.binance_id = None
        self.last_position_id = None
        self.all_orders_data = None
        self.trades_data = None
        self.transactions_data = None
        self.profile = None

    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info", {})
            kakao_id = user_info.get("kakao_id")

            binance_api_key = UserKeyInfoServices.get_binance_api_key(kakao_id)

            CollectServices.collect(kakao_id, binance_api_key)

            position_dto_lsit = PositionCalculatorServices.calculate_position(
                kakao_id, binance_api_key
            )

            TransactionServices.save_position(position_dto_lsit)

            profile = ProfileServices.get_profile(kakao_id)
        except Exception as e:
            print(f"Error in Collect.get(): {e}")
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "profile": profile,
            },
        )


class Profile(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = user_info["kakao_id"]
            profile = ProfileServices.get_profile(kakao_id)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "profile": profile,
            },
        )
