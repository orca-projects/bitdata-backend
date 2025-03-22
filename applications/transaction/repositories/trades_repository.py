import logging
import traceback

from applications.transaction.models import Trades


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# Trades 테이블 관리 Repository
class TradesRepository:
    @staticmethod
    def get_last_trades_id():
        try:
            last_trade = Trades.objects.order_by("-trade_id").first()
            return last_trade.trade_id if last_trade else 0  # 데이터가 없으면 0 반환
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"마지막 Trades ID 조회 중 오류 발생: {e}\n{error_trace}")
            return 0  # 오류 발생 시 기본값 0 반환

    # 25.02.18 윤택한
    # Trades Data 저장
    @staticmethod
    def create(binance_id, trades_data):
        try:
            if not trades_data:
                logger.warning("Trades 데이터 없음")
                return None

            trades_objects = [
                Trades(binance_id=binance_id, **trade) for trade in trades_data
            ]

            Trades.objects.bulk_create(trades_objects)
            logger.info(f"{len(trades_objects)}개의 Trades 데이터를 저장했습니다.")

        except Exception as e:
            logger.error(f"Trades 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("Trades 데이터 저장 중 오류 발생")
