import logging
import traceback
from django.db import connection
from django.utils import timezone
from applications.transaction.models import OrderHistory


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# OrderHistory 테이블 관리 Repository
class OrderHistoryRepository:
    # 25.02.18 윤택한
    # orders data 저장
    @staticmethod
    def set_order_history(binance_uid, orders_data):
        try:
            for order in orders_data:
                lookup = {
                    "binance_uid": binance_uid,
                    "symbol": order["symbol"],
                    "order_id": order["order_id"],
                }

                defaults = order.copy()

                for key in lookup.keys():
                    defaults.pop(key, None)

                defaults["updated_at"] = timezone.now()

                OrderHistory.objects.update_or_create(**lookup, defaults=defaults)
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"OrderHistory 데이터 저장 중 오류 발생: {e}\n{error_trace}")
            raise RuntimeError("OrderHistory 데이터 저장 중 오류 발생")

    @staticmethod
    def get_order_summary(binance_uid, last_closed_at):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                        WITH order_history_summary AS (
                            SELECT 
                                oh."id",
                                oh."orderId" AS order_id,
                                oh."symbol",
                                oh."side",
                                oh."executedQty"::NUMERIC * (CASE WHEN oh."side" = 'BUY' THEN 1 ELSE -1 END) AS executed_quantity,
                                oh."executedQty"::NUMERIC * oh."avgPrice"::NUMERIC AS size,
                                COALESCE(SUM(CASE WHEN tsh."incomeType" = 'COMMISSION' THEN CAST(tsh."income" AS NUMERIC) ELSE 0 END), 0) AS commission,
                                COALESCE(SUM(CASE WHEN tsh."incomeType" = 'REALIZED_PNL' THEN CAST(tsh."income" AS NUMERIC) ELSE 0 END), 0) AS realized_pnl,
                                MIN(trh."time") AS trade_start_time,
                                MAX(trh."time") AS trade_end_time
                            FROM "OrderHistory" AS oh
                            LEFT JOIN "TradeHistory" AS trh ON trh."binanceUid" = oh."binanceUid" AND trh."symbol" = oh."symbol" AND trh."orderId" = oh."orderId" 
                            LEFT JOIN "TransactionHistory" AS tsh ON tsh."binanceUid" = oh."binanceUid" AND tsh."symbol" = oh."symbol" AND tsh."tradeId" = trh."tradeId"
                            WHERE oh."binanceUid" = %s
                            GROUP BY oh."id", oh."binanceUid", oh."symbol", oh."orderId", oh."side", oh."executedQty", oh."avgPrice"
                        )
                        SELECT *
                        FROM order_history_summary
                        WHERE trade_start_time IS NOT NULL
                        AND trade_start_time >= %s
                        ORDER BY trade_start_time DESC;
                    """,
                    [binance_uid, last_closed_at],
                )
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"포지션 데이터 조회 중 오류 발생: {e}\n{error_trace}")
            return []
