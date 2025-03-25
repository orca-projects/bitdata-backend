from django.http import JsonResponse
from rest_framework.views import APIView
from core.utils import ResponseHelper

from applications.users.services import UserKeyInfoServices
from applications.transaction.services import TransactionServices


class Transaction(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info", {})
            kakao_id = user_info.get("kakao_id")

            binance_id = UserKeyInfoServices.get_binance_id(kakao_id)

            start_date = request.query_params.get("start_date")
            end_date = request.query_params.get("end_date")

            transaction = TransactionServices.get_position_by_date(
                binance_id, start_date, end_date
            )
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "transaction": transaction,
            },
        )
