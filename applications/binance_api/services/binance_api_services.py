import logging

from applications.transaction.repositories import OrdersRepository
from applications.transaction.repositories import TradesRepository
from applications.transaction.repositories import TransactionsRepository
from applications.binance_api.repositories import BinanceApiRepository


logger = logging.getLogger(__name__)


class BinanceApiServices:
    @staticmethod
    def is_connected(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        is_connected = BinanceApiRepository.is_connected(api_key, secret_key)

        return is_connected

    @staticmethod
    def get_binance_id(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        uid = BinanceApiRepository.get_binance_uid(api_key, secret_key)

        return uid

    @staticmethod
    def get_position_info_data(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        position_information = BinanceApiRepository.fetch_position_info_data(
            api_key, secret_key
        )

        return position_information

    @staticmethod
    def get_orders_data(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        last_order_id = OrdersRepository.get_last_order_id()

        raw_orders_data = BinanceApiRepository.fetch_orders_data(
            api_key, secret_key, int(last_order_id) + 1
        )

        orders_data = BinanceApiServices.process_orders_data(raw_orders_data)

        return orders_data

    @staticmethod
    def process_orders_data(raw_orders_data):
        orders_data = []

        for raw_order in raw_orders_data:
            try:
                order = {
                    "order_id": raw_order["orderId"],
                    "client_order_id": raw_order["clientOrderId"],
                    "avg_price": float(raw_order["avgPrice"]),
                    "executed_qty": float(raw_order["executedQty"]),
                    "orig_qty": float(raw_order["origQty"]),
                    "orig_type": raw_order["origType"],
                    "price": float(raw_order["price"]),
                    "reduce_only": raw_order["reduceOnly"],
                    "close_position": raw_order["closePosition"],
                    "side": raw_order["side"],
                    "position_side": raw_order["positionSide"],
                    "status": raw_order["status"],
                    "stop_price": float(raw_order.get("stopPrice", 0)),  # NULL 허용
                    "time": int(raw_order["time"]),
                    "time_in_force": raw_order["timeInForce"],
                    "type": raw_order["type"],
                    "update_time": int(raw_order["updateTime"]),
                    "working_type": raw_order["workingType"],
                    "price_protect": raw_order["priceProtect"],
                    "price_match": raw_order["priceMatch"],
                    "self_trade_prevention_mode": raw_order["selfTradePreventionMode"],
                    "good_till_date": int(raw_order.get("goodTillDate", 0)),  # 기본값 0
                    "cum_quote": float(raw_order.get("cumQuote", "0")),  # 기본값 '0'
                    "symbol": raw_order["symbol"],
                }
                orders_data.append(order)
            except KeyError as e:
                logger.warning(
                    f"주문 데이터 가공 중 키 에러 발생: {e} - 데이터: {order}"
                )
            except ValueError as e:
                logger.warning(f"주문 데이터 변환 중 오류 발생: {e} - 데이터: {order}")

        return orders_data

    @staticmethod
    def get_trades_data(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        last_trade_id = TradesRepository.get_last_trades_id()

        raw_trades_data = BinanceApiRepository.fetch_trades_data(api_key, secret_key, int(last_trade_id) + 1)

        trades_data = BinanceApiServices.process_trades_data(raw_trades_data)

        return trades_data
    
    @staticmethod
    def process_trades_data(raw_trades_data):
        trades_data = []

        for raw_trade in raw_trades_data:
            try:
                trade = {
                    "trade_id": raw_trade["id"],
                    "order_id": raw_trade["orderId"],
                    "symbol": raw_trade["symbol"],
                    "side": raw_trade["side"],
                    "price": float(raw_trade["price"]),
                    "qty": float(raw_trade["qty"]),
                    "realized_pnl": float(raw_trade["realizedPnl"]),
                    "quote_qty": float(raw_trade["quoteQty"]),
                    "commission": float(raw_trade["commission"]),
                    "commission_asset": raw_trade["commissionAsset"],
                    "time": int(raw_trade["time"]),
                    "position_side": raw_trade["positionSide"],
                    "buyer": raw_trade["buyer"],
                    "maker": raw_trade["maker"],
                }
                trades_data.append(trade)
            except KeyError as e:
                logger.warning(
                    f"trade 데이터 가공 중 키 에러 발생: {e} - 데이터: {trade}"
                )
            except ValueError as e:
                logger.warning(f"trade 데이터 변환 중 오류 발생: {e} - 데이터: {trade}")

        return trades_data

    @staticmethod
    def get_transactions_data(binance_api_key, start_time):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        raw_ransactions_data = BinanceApiRepository.fetch_income_history_data(
            api_key, secret_key, start_time
        )

        transactions_data = BinanceApiServices.process_transactions_data(raw_ransactions_data)

        return transactions_data

    @staticmethod
    def process_transactions_data(raw_ransactions_data):
        transactions_data = []

        for raw_transaction in raw_ransactions_data:
            try:
                transaction = {
                    "symbol": raw_transaction["symbol"] if raw_transaction["symbol"] else None,  # 빈 문자열 처리
                    "income_type": raw_transaction["incomeType"],
                    "income": float(raw_transaction["income"]),
                    "asset": raw_transaction["asset"],
                    "info": raw_transaction["info"],
                    "time": int(raw_transaction["time"]),  # timestamp로 변환
                    "tran_id": int(raw_transaction["tranId"]),
                    "trade_id": int(raw_transaction["tradeId"]) if raw_transaction["tradeId"] else None,  # 빈 문자열 처리
                }
                transactions_data.append(transaction)

            except KeyError as e:
                logger.warning(f"수익 데이터 가공 중 키 에러 발생: {e} - 데이터: {raw_transaction}")
            except ValueError as e:
                logger.warning(f"수익 데이터 변환 중 오류 발생: {e} - 데이터: {raw_transaction}")

        return transactions_data