from django.http import JsonResponse
from rest_framework.views import APIView
from core.utils import ResponseHelper

from applications.users.services import (
    UserApiKeyService,
    ProfileService,
)
from applications.transaction.services import (
    CollectService,
    PositionCalculatorService,
    TransactionService,
)


class BinanceKey(APIView):
    def post(self, request) -> JsonResponse:
        try:
            user_data = request.session.get("user_data")
            kakao_uid = user_data["kakao_uid"]
            binance_api_key = {
                "api_key": request.data.get("api_key"),
                "secret_key": request.data.get("secret_key"),
            }

            UserApiKeyService.save_binance_api_key(kakao_uid, binance_api_key)
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
            user_data = request.session.get("user_data", {})
            kakao_uid = user_data.get("kakao_uid")

            binance_api_key = UserApiKeyService.get_binance_api_key(kakao_uid)

            CollectService.collect(kakao_uid, binance_api_key)

            position_dto_lsit = PositionCalculatorService.calculate_position(
                kakao_uid, binance_api_key
            )

            TransactionService.save_position(position_dto_lsit)

            profile = ProfileService.get_profile(kakao_uid)
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
            user_data = request.session.get("user_data")
            kakao_uid = user_data["kakao_uid"]
            profile = ProfileService.get_profile(kakao_uid)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "profile": profile,
            },
        )
