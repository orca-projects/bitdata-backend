import logging
import traceback

from django.db import connection

from applications.transaction.models import Orders


logger = logging.getLogger(__name__)


# 25.02.18 윤택한
# Orders 테이블 관리 Repository
class OrdersRepository:
    # 25.02.18 윤택한
    # orders data 저장
    @staticmethod
    def create(binance_id, orders_data):
        try:
            if not orders_data:
                logger.warning("주문 데이터 없음")
                return None

            orders_objects = [
                Orders(binance_id=binance_id, **order) for order in orders_data
            ]

            Orders.objects.bulk_create(orders_objects)
            logger.info(f"{len(orders_objects)}개의 Orders 데이터를 저장했습니다.")

        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"Orders 데이터 저장 중 오류 발생: {e}\n{error_trace}")
            raise RuntimeError("Orders 데이터 저장 중 오류 발생")

    @staticmethod
    def get_order_summary(binance_id, after_order_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                        WITH order_summary AS (
                            SELECT 
                                o."id",
                                o."orderId" AS order_id,
                                o."symbol",
                                o."side",
                                o."executedQty"::NUMERIC * (CASE WHEN o."side" = 'BUY' THEN 1 ELSE -1 END) AS executed_quantity,
                                o."executedQty"::NUMERIC * o."avgPrice"::NUMERIC AS size,
                                COALESCE(SUM(CASE WHEN ts."incomeType" = 'COMMISSION' THEN CAST(ts."income" AS NUMERIC) ELSE 0 END), 0) AS commission,
                                COALESCE(SUM(CASE WHEN ts."incomeType" = 'REALIZED_PNL' THEN CAST(ts."income" AS NUMERIC) ELSE 0 END), 0) AS realized_pnl,
                                o."time"
                            FROM "Orders" AS o
                            LEFT JOIN "Trades" AS tr ON tr."binanceId" = o."binanceId" AND tr."symbol" = o."symbol" AND tr."orderId" = o."orderId" 
                            LEFT JOIN "Transactions" AS ts ON ts."binanceId" = o."binanceId"  AND ts."symbol" = o."symbol" AND ts."tradeId" = tr."tradeId"
                            WHERE o."binanceId" = %s
                            AND o."time" >= %s
                            GROUP BY o."id", o."binanceId", o."symbol", o."orderId", o."side", o."executedQty", o."avgPrice", o."time"
                        )
                        SELECT *
                        FROM order_summary
                        WHERE commission != 0
                        ORDER BY "time" DESC
                    """,
                    [binance_id, after_order_id],
                )
                columns = [col[0] for col in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except Exception as e:
            error_trace = traceback.format_exc()
            logger.error(f"포지션 데이터 조회 중 오류 발생: {e}\n{error_trace}")
            return []
