import logging
import traceback
from decimal import Decimal

from django.conf import settings
from django.db import connection

from applications.transaction.models import TransactionHistory


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# TransactionHistory 테이블 관리 Repository
class TransactionHistoryRepository:
    @staticmethod
    def get_last_time_by_binance_uid(binance_uid):
        try:
            last_income = (
                TransactionHistory.objects.filter(binance_uid=binance_uid)
                .order_by("-time")
                .first()
            )

            if last_income:
                return last_income.time.timestamp()
            else:
                return settings.BINANCE_DEFAULT_TIME

        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"마지막 거래 시간 조회 중 오류 발생: {e}\n{error_trace}")
            return settings.BINANCE_DEFAULT_TIME  # 오류 발생 시 기본값 반환

    # 25.02.18 윤택한
    # TransactionHistory Data 저장
    @staticmethod
    def set_transaction_history(binance_uid, transactions_data):
        try:
            transactions_objects = [
                TransactionHistory(binance_uid=binance_uid, **transaction)
                for transaction in transactions_data
            ]

            TransactionHistory.objects.bulk_create(
                transactions_objects, ignore_conflicts=True
            )
        except Exception as e:
            logger.error(f"TransactionHistory 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("TransactionHistory 데이터 저장 중 오류 발생")

    @staticmethod
    def get_total_funding_fee(symbol, start_time, end_time) -> Decimal:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT SUM(ts."income"::NUMERIC)
                    FROM "TransactionHistory" AS ts
                    WHERE ts."symbol" = %s
                    AND ts."time" BETWEEN %s AND %s
                    AND ts."incomeType" = 'FUNDING_FEE'
                    """,
                    [symbol, start_time, end_time],
                )
                row = cursor.fetchone()
                return row[0] if row[0] is not None else Decimal("0")

        except Exception as e:
            logger.error("Funding Fee 총합 계산 중 오류 발생", exc_info=True)
            return Decimal("0")
