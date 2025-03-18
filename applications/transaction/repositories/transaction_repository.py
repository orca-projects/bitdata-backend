import logging
import traceback


from applications.users.models import Transactions


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# Transactions 테이블 관리 Repository
class TransactionsRepository:
    @staticmethod
    def get_last_income_time():
        try:
            last_income = Transactions.objects.order_by("-time").first()
            return last_income.time if last_income else 1564588800001  # 데이터 없으면 기본값 1564588800001 반환
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"마지막 거래 시간 조회 중 오류 발생: {e}\n{error_trace}")
            return 1564588800001  # 오류 발생 시 기본값 1564588800001 반환

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
