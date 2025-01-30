from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils import ResponseHelper

from applications.users.services import UserServices
from applications.binance_api.services import BinanceApiServices


class BinanceKey(APIView):
    def post(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = UserServices.get_kakao_id(user_info)
            binance_api_key = {
                "api_key": request.data.get("api_key"),
                "secret_key": request.data.get("secret_key"),
            }

            UserServices.save_binance_api_key(kakao_id, binance_api_key)
        except Exception as e:
            return ResponseHelper.error(
                request=request,
                message="An error occurred",
                error_details=str(e),
            )

        return ResponseHelper.success(request=request)


class Collect(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.binance_uid = None

    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = UserServices.get_kakao_id(user_info)
            binance_api_key = UserServices.get_binance_api_key(kakao_id)

            self.collect(binance_api_key)
            self.save(kakao_id)

            profile = UserServices.get_profile(kakao_id)
        except Exception as e:
            return ResponseHelper.error(
                request=request,
                message="An error occurred",
                error_details=str(e),
            )

        return ResponseHelper.success(
            request=request,
            data={
                "profile": profile,
            },
        )

    def collect(self, binance_api_key):
        self.binanace_uid = BinanceApiServices.get_uid(binance_api_key)

    def save(self, kakao_id):
        if self.binance_uid:
            UserServices.save_binance_uid(kakao_id, self.binance_uid)


class Profile(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = UserServices.get_kakao_id(user_info)
            profile = UserServices.get_profile(kakao_id)
        except Exception as e:
            return ResponseHelper.error(
                request=request,
                message="An error occurred",
                error_details=str(e),
            )

        return ResponseHelper.success(
            request=request,
            data={
                "profile": profile,
            },
        )
