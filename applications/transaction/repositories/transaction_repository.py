import logging
import traceback
from decimal import Decimal

from django.conf import settings
from django.db import connection

from applications.transaction.models import Transactions


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# Transactions 테이블 관리 Repository
class TransactionsRepository:
    @staticmethod
    def get_last_time():
        try:
            last_income = Transactions.objects.order_by("-time").first()
            return (
                last_income.time if last_income else settings.BINANCE_DEFAULT_TIME
            )  # 데이터 없으면 기본값 반환
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"마지막 거래 시간 조회 중 오류 발생: {e}\n{error_trace}")
            return settings.BINANCE_DEFAULT_TIME  # 오류 발생 시 기본값 반환

    # 25.02.18 윤택한
    # Transactions Data 저장
    @staticmethod
    def create(binance_id, transactions_data):
        try:
            if not transactions_data:
                logger.warning("거래 내역 데이터 없음")
                return None

            transactions_objects = [
                Transactions(binance_id=binance_id, **transaction)
                for transaction in transactions_data
            ]

            Transactions.objects.bulk_create(
                transactions_objects, ignore_conflicts=True
            )
            logger.info(
                f"{len(transactions_objects)}개의 Transactions 데이터를 저장했습니다."
            )

        except Exception as e:
            logger.error(f"Transactions 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("Transactions 데이터 저장 중 오류 발생")

    @staticmethod
    def get_total_funding_fee(symbol, start_time, end_time) -> Decimal:
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT SUM(ts."income"::NUMERIC)
                    FROM "Transactions" AS ts
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
