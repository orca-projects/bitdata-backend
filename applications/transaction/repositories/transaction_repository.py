import logging
import traceback

from applications.users.models import Transactions


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# Transactions 테이블 관리 Repository
class TransactionsRepository:
    # 25.02.18 윤택한
    # Transactions Data 저장
    @staticmethod
    def save_transactions_data(binance_id, transactions_data):
        try:
            if not transactions_data:
                logger.warning("거래 내역 데이터 없음")
                return None

            transactions_objects = [
                Transactions(binance_id=binance_id, **transaction) for transaction in transactions_data
            ]

            Transactions.objects.bulk_create(transactions_objects)
            logger.info(
                f"{len(transactions_objects)}개의 Transactions 데이터를 저장했습니다."
            )

        except Exception as e:
            logger.error(f"Transactions 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("Transactions 데이터 저장 중 오류 발생")

    # 25.02.28(금) 윤택한
    # transactoin_datas 가져오기
    @staticmethod
    def get_transactions_by_binance_id(binance_id):
        try:
            return Transactions.objects.filter(binance_id=binance_id).all()
        except Exception as e:
            logger.error(f"Transactions 데이터 조회 중 오류 발생: {e}")
            return None
