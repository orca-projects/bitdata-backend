import logging
from decimal import Decimal
from applications.transaction.repositories import (
    TransactionsRepository,
)
from applications.binance_api.repositories import BinanceApiRepository

logger = logging.getLogger(__name__)


class BinanceApiServices:
    @staticmethod
    def is_connected(binance_api_key: dict) -> bool:
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]
        return BinanceApiRepository.is_connected(api_key, secret_key)

    @staticmethod
    def get_binance_id(binance_api_key: dict) -> str:
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]
        return BinanceApiRepository.get_binance_uid(api_key, secret_key)

    @staticmethod
    def get_orders_data(binance_api_key: dict) -> list[dict]:
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        raw_data = BinanceApiRepository.fetch_orders_data(api_key, secret_key)
        return BinanceApiServices.process_orders_data(raw_data)

    @staticmethod
    def process_orders_data(raw_orders_data: list) -> list[dict]:
        orders = []

        for item in raw_orders_data:
            try:
                order = {
                    "order_id": item["orderId"],
                    "client_order_id": item["clientOrderId"],
                    "avg_price": Decimal(item["avgPrice"]),
                    "executed_qty": Decimal(item["executedQty"]),
                    "orig_qty": Decimal(item["origQty"]),
                    "orig_type": item["origType"],
                    "price": Decimal(item["price"]),
                    "reduce_only": item["reduceOnly"],
                    "close_position": item["closePosition"],
                    "side": item["side"],
                    "position_side": item["positionSide"],
                    "status": item["status"],
                    "stop_price": Decimal(item.get("stopPrice") or "0"),
                    "time": int(item["time"]),
                    "time_in_force": item["timeInForce"],
                    "type": item["type"],
                    "update_time": int(item["updateTime"]),
                    "working_type": item["workingType"],
                    "price_protect": item["priceProtect"],
                    "price_match": item["priceMatch"],
                    "self_trade_prevention_mode": item["selfTradePreventionMode"],
                    "good_till_date": int(item.get("goodTillDate") or 0),
                    "cum_quote": Decimal(item.get("cumQuote") or "0"),
                    "symbol": item["symbol"],
                }
                orders.append(order)
            except (KeyError, ValueError) as e:
                logger.warning(
                    f"[Orders] 데이터 가공 중 오류 발생: {e} - 데이터: {item}"
                )

        return orders

    @staticmethod
    def get_trades_data(binance_api_key: dict) -> list[dict]:
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        raw_data = BinanceApiRepository.fetch_trades_data(api_key, secret_key)
        return BinanceApiServices.process_trades_data(raw_data)

    @staticmethod
    def process_trades_data(raw_trades_data: list) -> list[dict]:
        trades = []

        for item in raw_trades_data:
            try:
                trade = {
                    "trade_id": item["id"],
                    "order_id": item["orderId"],
                    "symbol": item["symbol"],
                    "side": item["side"],
                    "price": Decimal(item["price"]),
                    "qty": Decimal(item["qty"]),
                    "realized_pnl": Decimal(item["realizedPnl"]),
                    "quote_qty": Decimal(item["quoteQty"]),
                    "commission": Decimal(item["commission"]),
                    "commission_asset": item["commissionAsset"],
                    "time": int(item["time"]),
                    "position_side": item["positionSide"],
                    "buyer": item["buyer"],
                    "maker": item["maker"],
                }
                trades.append(trade)
            except (KeyError, ValueError) as e:
                logger.warning(
                    f"[Trades] 데이터 가공 중 오류 발생: {e} - 데이터: {item}"
                )

        return trades

    @staticmethod
    def get_transactions_data(binance_api_key: dict) -> list[dict]:
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        last_time = TransactionsRepository.get_last_time()
        raw_data = BinanceApiRepository.fetch_income_history_data(
            api_key, secret_key, last_time
        )
        return BinanceApiServices.process_transactions_data(raw_data)

    @staticmethod
    def process_transactions_data(raw_transactions_data: list) -> list[dict]:
        transactions = []

        for item in raw_transactions_data:
            try:
                transaction = {
                    "symbol": item["symbol"] or None,
                    "income_type": item["incomeType"],
                    "income": Decimal(item["income"]),
                    "asset": item["asset"],
                    "info": item["info"],
                    "time": int(item["time"]),
                    "tran_id": int(item["tranId"]),
                    "trade_id": int(item["tradeId"]) if item["tradeId"] else None,
                }
                transactions.append(transaction)
            except (KeyError, ValueError) as e:
                logger.warning(
                    f"[Transactions] 데이터 가공 중 오류 발생: {e} - 데이터: {item}"
                )

        return transactions

    @staticmethod
    def get_position_info_data(binance_api_key: dict) -> list[dict]:
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        raw_data = BinanceApiRepository.fetch_position_info_data(api_key, secret_key)
        return BinanceApiServices.process_position_info_data(raw_data)

    @staticmethod
    def process_position_info_data(raw_position_data: list) -> list[dict]:
        positions = []

        for item in raw_position_data:
            try:
                position = {
                    "symbol": item["symbol"],
                    "position_side": item["positionSide"],
                    "position_amt": Decimal(item["positionAmt"]),
                    "entry_price": Decimal(item["entryPrice"]),
                    "break_even_price": Decimal(item.get("breakEvenPrice") or "0"),
                    "mark_price": Decimal(item["markPrice"]),
                    "unrealized_profit": Decimal(item["unRealizedProfit"]),
                    "initial_margin": Decimal(item["initialMargin"]),
                    "maint_margin": Decimal(item["maintMargin"]),
                    "position_initial_margin": Decimal(item["positionInitialMargin"]),
                    "update_time": int(item["updateTime"]),
                }
                positions.append(position)
            except (KeyError, ValueError) as e:
                logger.warning(
                    f"[Positions] 데이터 가공 중 오류 발생: {e} - 데이터: {item}"
                )

        return positions
