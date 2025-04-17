import logging
from django.db.models import Max
from applications.users.models import Orders, Trades, Transactions, PositionOrders
from datetime import datetime
from django.utils.timezone import make_aware
from django.db import transaction
from django.db import IntegrityError


logger = logging.getLogger(__name__)


# 25.02.26 윤택한
# Position 테이블 관리 Repository
class PositionOrdersRepository:
    # 25.02.26 윤택한
    # 해당 테이블에서 받아온 binance_id가 가지고 있는 positionId의 최대 값을 return
    @staticmethod
    def get_max_position_id(binance_id):
        try:
            max_position = PositionOrders.objects.filter(
                binance_id=binance_id
            ).aggregate(Max("position_id"))
            max_position_id = max_position.get("position_id__max")

            if max_position_id is None:
                logger.info(f"No positions found for binance_id: {binance_id}")
                return 0  # 기본값 0 반환

            return max_position_id  # int 값 반환

        except Exception as e:
            logger.error(f"Position ID 조회 중 오류 발생: {e}")
            return 0  # 오류 발생 시 기본값 반환

    # 25.02.27(목) 윤택한
    # positions_data 저장
    @staticmethod
    def save_positions_data(positions_data):
        try:
            if not positions_data:
                logger.warning("저장할 positions_data가 없습니다.")
                return None

            position_objects = [
                PositionOrders(
                    binance_id=data["binanceId"],
                    order_id=data["orderId"],
                    position_id=data["positionId"],
                )
                for data in positions_data
            ]

            with transaction.atomic():  # 트랜잭션 처리 (데이터 일관성 유지)
                PositionOrders.objects.bulk_create(position_objects)

            logger.info(f"{len(positions_data)}개의 Position 데이터 저장 완료")
            return True

        except Exception as e:
            logger.error(f"Position 데이터 저장 중 오류 발생: {e}")
            return None

    # 25.02.28(금) 윤택한
    # positions_datas 가져오기
    @staticmethod
    def get_positions(binance_id):
        try:
            return PositionOrders.objects.filter(binance_id=binance_id)
        except Exception as e:
            logger.error(f"포지션 데이터 조회 중 오류 발생: {e}")
            return None


# 25.02.18 윤택한
# Orders 테이블 관리 Repository
class OrdersRepository:
    # 25.02.18 윤택한
    # orders data 저장
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

    # 25.02.28(금) 윤택한
    # orders_datas 가져오기
    @staticmethod
    def get_order_by_order_id(order_id):
        try:
            return Orders.objects.get(order_id=order_id)
        except Orders.DoesNotExist:
            logger.error(
                f"Order ID {order_id}에 대한 Orders 데이터가 존재하지 않습니다."
            )
            return None
        except Exception as e:
            logger.error(f"Orders 데이터 조회 중 오류 발생: {e}")
            return None

    @staticmethod
    def get_orders_by_order_ids(order_ids):
        try:
            return Orders.objects.filter(order_id__in=order_ids).order_by("time")
        except Exception as e:
            logger.error(f"Orders 데이터 조회 중 오류 발생: {e}")
            return None

    @staticmethod
    def upsert_orders_data(binance_id, orders_data):
        if not orders_data:
            return

        for order in orders_data:
            try:
                Orders.objects.update_or_create(
                    binance_id_id=binance_id,
                    symbol=order["symbol"],
                    order_id=order["orderId"],
                    defaults={
                        "client_order_id": order["clientOrderId"],
                        "avg_price": order["avgPrice"],
                        "executed_qty": order["executedQty"],
                        "orig_qty": order["origQty"],
                        "orig_type": order["origType"],
                        "price": order["price"],
                        "reduce_only": order["reduceOnly"],
                        "close_position": order["closePosition"],
                        "side": order["side"],
                        "position_side": order["positionSide"],
                        "status": order["status"],
                        "stop_price": order.get("stopPrice", None),
                        "time": order["time"],
                        "time_in_force": order["timeInForce"],
                        "type": order["type"],
                        "update_time": order["updateTime"],
                        "working_type": order["workingType"],
                        "price_protect": order["priceProtect"],
                        "price_match": order["priceMatch"],
                        "self_trade_prevention_mode": order["selfTradePreventionMode"],
                        "good_till_date": order.get("goodTillDate", 0),
                        "cum_quote": order.get("cumQuote", "0"),
                    },
                )
            except IntegrityError as e:
                logger.warning(f"Order upsert 실패: {e}")


# 25.02.18 윤택한
# Trades 테이블 관리 Repository
class TradesRepository:
    # 25.02.18 윤택한
    # Trades Data 저장
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

    # 25.02.28(금) 윤택한
    # trades_datas 가져오기
    @staticmethod
    def get_trades_by_binance_id(binance_id):
        try:
            return Trades.objects.filter(binance_id=binance_id).all()
        except Exception as e:
            logger.error(f"Trades 데이터 조회 중 오류 발생: {e}")
            return None

    @staticmethod
    def get_trades_by_binance_id_and_order_ids(binance_id, order_ids):
        try:
            return Trades.objects.filter(binance_id=binance_id, order_id__in=order_ids)
        except Exception as e:
            logger.error(f"Trades 데이터 조회 중 오류 발생: {e}")
            return None

    @staticmethod
    def upsert_trades_data(binance_id, trades_data):
        if not trades_data:
            return
        for trade in trades_data:
            try:
                Trades.objects.update_or_create(
                    binance_id_id=binance_id,
                    symbol=trade["symbol"],
                    trade_id=trade["id"],
                    defaults={
                        "order_id": trade["orderId"],
                        "side": trade["side"],
                        "price": trade["price"],
                        "qty": trade["qty"],
                        "realized_pnl": trade["realizedPnl"],
                        "quote_qty": trade["quoteQty"],
                        "commission": trade["commission"],
                        "commission_asset": trade["commissionAsset"],
                        "time": trade["time"],
                        "position_side": trade["positionSide"],
                        "buyer": trade["buyer"],
                        "maker": trade["maker"],
                    },
                )
            except IntegrityError as e:
                logger.warning(f"Trade upsert 실패: {e}")


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
                Transactions(
                    binance_id_id=binance_id,
                    symbol=(
                        txn["symbol"] if txn["symbol"] else None
                    ),  # 빈 문자열이면 None 처리
                    income_type=txn["incomeType"],
                    income=txn["income"],
                    asset=txn["asset"],
                    info=txn["info"],
                    time=txn["time"],
                    tran_id=txn["tranId"],
                    trade_id=(
                        txn["tradeId"] if txn["tradeId"] else None
                    ),  # 빈 문자열이면 None 처리
                )
                for txn in transactions_data
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

    @staticmethod
    def upsert_transactions_data(binance_id, transactions_data):
        if not transactions_data:
            return
        for txn in transactions_data:
            try:
                Transactions.objects.update_or_create(
                    binance_id_id=binance_id,
                    symbol=txn.get("symbol") or None,
                    tran_id=txn["tranId"],
                    income_type=txn["incomeType"],
                    defaults={
                        "income": txn["income"],
                        "asset": txn["asset"],
                        "info": txn["info"],
                        "time": txn["time"],
                        "trade_id": txn.get("tradeId") or None,
                    },
                )
            except IntegrityError as e:
                logger.warning(f"Transaction upsert 실패: {e}")
