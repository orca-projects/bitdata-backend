from django.http import JsonResponse
from rest_framework.views import APIView
from core.utils import ResponseUtil

from applications.users.services import (
    UserService,
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
            return ResponseUtil.error()

        return ResponseUtil.success()


class Collect(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_data = request.session.get("user_data")
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
            return ResponseUtil.error(
                data={
                    "profile": {},
                },
            )

        return ResponseUtil.success(
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
            return ResponseUtil.error()

        return ResponseUtil.success(
            data={
                "profile": profile,
            },
        )


class Withdraw(APIView):
    def post(self, request) -> JsonResponse:
        try:
            user_data = request.session.get("user_data")
            kakao_uid = user_data["kakao_uid"]
            reason = request.data.get("withdraw_reason", "")

            result = UserService.withdraw(request, kakao_uid, reason)

            return ResponseUtil.success(data={"result": result})
        except Exception as e:
            print(e)
            return ResponseUtil.error()
