from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils import ResponseHelper

from applications.users.services import UserServices
from applications.binance_api.services import BinanceApiServices


class BinanceKey(APIView):
    def post(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = user_info["kakao_id"]
            binance_api_key = {
                "api_key": request.data.get("api_key"),
                "secret_key": request.data.get("secret_key"),
            }

            UserServices.save_binance_api_key(kakao_id, binance_api_key)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success()


class Collect(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_connected = True
        self.binance_id = None

    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = user_info["kakao_id"]
            binance_api_key = UserServices.get_binance_api_key(kakao_id)

            self.collect(binance_api_key)
            self.save(kakao_id)

            profile = UserServices.get_profile(kakao_id)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "profile": profile,
            },
        )

    def collect(self, binance_api_key):
        self.is_connected = BinanceApiServices.is_connected(binance_api_key)

        if self.is_connected:
            self.binance_id = BinanceApiServices.get_binance_id(binance_api_key)

    def save(self, kakao_id):
        UserServices.save_is_connected(kakao_id, self.is_connected)
        UserServices.save_binance_id(kakao_id, self.binance_id)


class Profile(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = user_info["kakao_id"]
            profile = UserServices.get_profile(kakao_id)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "profile": profile,
            },
        )
