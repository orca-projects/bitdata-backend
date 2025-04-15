import logging
import traceback

from applications.transaction.models import TradeHistory


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# TradeHistory 테이블 관리 Repository
class TradeHistoryRepository:
    # 25.02.18 윤택한
    # TradeHistory Data 저장
    @staticmethod
    def create(binance_id, trades_data):
        try:
            if not trades_data:
                logger.warning("TradeHistory 데이터 없음")
                return None

            trades_objects = [
                TradeHistory(binance_id=binance_id, **trade) for trade in trades_data
            ]

            TradeHistory.objects.bulk_create(trades_objects)
            logger.info(
                f"{len(trades_objects)}개의 TradeHistory 데이터를 저장했습니다."
            )

        except Exception as e:
            logger.error(f"TradeHistory 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("TradeHistory 데이터 저장 중 오류 발생")
