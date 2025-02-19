import logging

from applications.users.models import Orders, Trades, Transactions
from datetime import datetime
from django.utils.timezone import make_aware


logger = logging.getLogger(__name__)
# 25.02.18 윤택한
# Orders 데이터 저장하는 클래스
class OrdersRepository:
    @staticmethod
    def save_orders_data(binance_id, orders_data):
        try:
            if not orders_data:
                logger.warning("주문 데이터 없음")
                return None
            
            orders_objects = [
                Orders(
                    binance_id_id=binance_id,
                    order_id=order["orderId"],
                    client_order_id=order["clientOrderId"],
                    avg_price=order["avgPrice"],
                    executed_qty=order["executedQty"],
                    orig_qty=order["origQty"],
                    orig_type=order["origType"],
                    price=order["price"],
                    reduce_only=order["reduceOnly"],
                    close_position=order["closePosition"],
                    side=order["side"],
                    position_side=order["positionSide"],
                    status=order["status"],
                    stop_price=order.get("stopPrice", None),  # NULL 허용
                    time=order["time"],
                    time_in_force=order["timeInForce"],
                    type=order["type"],
                    update_time=order["updateTime"],
                    working_type=order["workingType"],
                    price_protect=order["priceProtect"],
                    price_match=order["priceMatch"],
                    self_trade_prevention_mode=order["selfTradePreventionMode"],
                    good_till_date=order.get("goodTillDate", 0),  # 기본값 0
                    cum_quote=order.get("cumQuote", "0"),  # 기본값 '0'
                    symbol=order["symbol"],
                )
                for order in orders_data
            ]

            Orders.objects.bulk_create(orders_objects)
            logger.info(f"{len(orders_objects)}개의 Orders 데이터를 저장했습니다.")

        except Exception as e:
            logger.error(f"Orders 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("Orders 데이터 저장 중 오류 발생")
# 25.02.18 윤택한
# Trades 데이터 저장하는 클래스
class TradesRepository:
    @staticmethod
    def save_trades_data(binance_id, trades_data):
        try:
            if not trades_data:
                logger.warning("Trades 데이터 없음")
                return None

            trades_objects = [
                Trades(
                    binance_id_id=binance_id,
                    trade_id=trade["id"],
                    order_id=trade["orderId"],
                    symbol=trade["symbol"],
                    side=trade["side"],
                    price=trade["price"],
                    qty=trade["qty"],
                    realized_pnl=trade["realizedPnl"],
                    quote_qty=trade["quoteQty"],
                    commission=trade["commission"],
                    commission_asset=trade["commissionAsset"],
                    time=trade["time"],
                    position_side=trade["positionSide"],
                    buyer=trade["buyer"],
                    maker=trade["maker"],
                )
                for trade in trades_data
            ]

            Trades.objects.bulk_create(trades_objects)
            logger.info(f"{len(trades_objects)}개의 Trades 데이터를 저장했습니다.")

        except Exception as e:
            logger.error(f"Trades 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("Trades 데이터 저장 중 오류 발생")
# 25.02.18 윤택한
# Transactions 데이터 저장하는 클래스
class TransactionsRepository:
    @staticmethod
    def save_transactions_data(binance_id, transactions_data):
        try:
            if not transactions_data:
                logger.warning("거래 내역 데이터 없음")
                return None

            transactions_objects = [
                Transactions(
                    binance_id_id=binance_id,
                    symbol=txn["symbol"] if txn["symbol"] else None,  # 빈 문자열이면 None 처리
                    income_type=txn["incomeType"],
                    income=txn["income"],
                    asset=txn["asset"],
                    info=txn["info"],
                    time=txn["time"],
                    tran_id=txn["tranId"],
                    trade_id=txn["tradeId"] if txn["tradeId"] else None,  # 빈 문자열이면 None 처리
                )
                for txn in transactions_data
            ]

            Transactions.objects.bulk_create(transactions_objects)
            logger.info(f"{len(transactions_objects)}개의 Transactions 데이터를 저장했습니다.")

        except Exception as e:
            logger.error(f"Transactions 데이터 저장 중 오류 발생: {e}")
            raise RuntimeError("Transactions 데이터 저장 중 오류 발생")