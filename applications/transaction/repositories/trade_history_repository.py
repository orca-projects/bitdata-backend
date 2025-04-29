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
    def set_trade_history(binance_uid, trades_data):
        try:
            trades_objects = [
                TradeHistory(binance_uid=binance_uid, **trade) for trade in trades_data
            ]

            TradeHistory.objects.bulk_create(trades_objects, ignore_conflicts=True)
        except Exception as e:
            logger.error(f"TradeHistory 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("TradeHistory 데이터 저장 중 오류 발생")
