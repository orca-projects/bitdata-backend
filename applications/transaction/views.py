from django.http import JsonResponse
from rest_framework.views import APIView
from core.utils import ResponseUtil

from applications.users.services import UserApiKeyService
from applications.transaction.services import TransactionService


class Transaction(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_data = request.session.get("user_data", {})
            kakao_uid = user_data.get("kakao_uid")

            binance_uid = UserApiKeyService.get_binance_uid(kakao_uid)

            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")

            transaction = TransactionService.get_position_by_date(
                binance_uid, start_date, end_date
            )
        except Exception as e:
            print(e)
            return ResponseUtil.error()

        return ResponseUtil.success(
            data={
                "transaction": transaction,
            },
        )
