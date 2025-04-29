import logging
from decimal import Decimal
from core.utils import DateUtil
from applications.transaction.repositories import TransactionHistoryRepository
from applications.binance_api.repositories import BinanceApiRepository

logger = logging.getLogger(__name__)


class BinanceApiServices:
    @staticmethod
    def _get_keys(binance_api_key: dict) -> tuple[str, str]:
        return binance_api_key["api_key"], binance_api_key["secret_key"]

    @staticmethod
    def is_connected(binance_api_key: dict) -> bool:
        api_key, secret_key = BinanceApiServices._get_keys(binance_api_key)
        return BinanceApiRepository.is_connected(api_key, secret_key)

    @staticmethod
    def get_binance_uid(binance_api_key: dict) -> str:
        api_key, secret_key = BinanceApiServices._get_keys(binance_api_key)
        return BinanceApiRepository.get_binance_uid(api_key, secret_key)

    @staticmethod
    def get_orders_data(binance_api_key: dict) -> list[dict]:
        api_key, secret_key = BinanceApiServices._get_keys(binance_api_key)
        raw_data = BinanceApiRepository.fetch_orders_data(api_key, secret_key)
        return BinanceApiServices.process_orders_data(raw_data)

    @staticmethod
    def process_orders_data(raw_orders_data: list[dict]) -> list[dict]:
        orders = []

        for item in raw_orders_data:
            try:
                orders.append(
                    {
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
                        "time": DateUtil.parse_timestamp_to_datetime(item["time"]),
                        "time_in_force": item["timeInForce"],
                        "type": item["type"],
                        "update_time": DateUtil.parse_timestamp_to_datetime(
                            item["updateTime"]
                        ),
                        "working_type": item["workingType"],
                        "price_protect": item["priceProtect"],
                        "price_match": item["priceMatch"],
                        "self_trade_prevention_mode": item["selfTradePreventionMode"],
                        "good_till_date": int(item.get("goodTillDate") or 0),
                        "cum_quote": Decimal(item.get("cumQuote") or "0"),
                        "symbol": item["symbol"],
                    }
                )
            except (KeyError, ValueError) as e:
                logger.warning(f"[Order] 데이터 가공 오류: {e} - {item}")

        return orders

    @staticmethod
    def get_trades_data(binance_api_key: dict) -> list[dict]:
        api_key, secret_key = BinanceApiServices._get_keys(binance_api_key)
        raw_data = BinanceApiRepository.fetch_trades_data(api_key, secret_key)
        return BinanceApiServices.process_trades_data(raw_data)

    @staticmethod
    def process_trades_data(raw_trades_data: list[dict]) -> list[dict]:
        trades = []

        for item in raw_trades_data:
            try:
                trades.append(
                    {
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
                        "time": DateUtil.parse_timestamp_to_datetime(item["time"]),
                        "position_side": item["positionSide"],
                        "buyer": item["buyer"],
                        "maker": item["maker"],
                    }
                )
            except (KeyError, ValueError) as e:
                logger.warning(f"[Trade] 데이터 가공 오류: {e} - {item}")

        return trades

    @staticmethod
    def get_transactions_data(binance_uid, binance_api_key: dict) -> list[dict]:
        api_key, secret_key = BinanceApiServices._get_keys(binance_api_key)
        last_time = TransactionHistoryRepository.get_last_time_by_binance_uid(
            binance_uid
        )
        raw_data = BinanceApiRepository.fetch_income_history_data(
            api_key, secret_key, last_time
        )
        return BinanceApiServices.process_transactions_data(raw_data)

    @staticmethod
    def process_transactions_data(raw_transactions_data: list[dict]) -> list[dict]:
        transactions = []

        for item in raw_transactions_data:
            try:
                transactions.append(
                    {
                        "symbol": item.get("symbol") or None,
                        "income_type": item["incomeType"],
                        "income": Decimal(item["income"]),
                        "asset": item["asset"],
                        "info": item.get("info") or "",
                        "time": DateUtil.parse_timestamp_to_datetime(item["time"]),
                        "tran_id": int(item["tranId"]),
                        "trade_id": (
                            int(item["tradeId"]) if item.get("tradeId") else None
                        ),
                    }
                )
            except (KeyError, ValueError) as e:
                logger.warning(f"[Transaction] 데이터 가공 오류: {e} - {item}")

        return transactions

    @staticmethod
    def get_position_info_data(binance_api_key: dict) -> list[dict]:
        api_key, secret_key = BinanceApiServices._get_keys(binance_api_key)
        raw_data = BinanceApiRepository.fetch_position_info_data(api_key, secret_key)
        return BinanceApiServices.process_position_info_data(raw_data)

    @staticmethod
    def process_position_info_data(raw_position_data: list[dict]) -> list[dict]:
        positions = []

        for item in raw_position_data:
            try:
                positions.append(
                    {
                        "symbol": item["symbol"],
                        "position_side": item["positionSide"],
                        "position_amt": Decimal(item["positionAmt"]),
                        "entry_price": Decimal(item["entryPrice"]),
                        "break_even_price": Decimal(item.get("breakEvenPrice") or "0"),
                        "mark_price": Decimal(item["markPrice"]),
                        "unrealized_profit": Decimal(item["unRealizedProfit"]),
                        "initial_margin": Decimal(item["initialMargin"]),
                        "maint_margin": Decimal(item["maintMargin"]),
                        "position_initial_margin": Decimal(
                            item["positionInitialMargin"]
                        ),
                        "update_time": DateUtil.parse_timestamp_to_datetime(
                            item["updateTime"]
                        ),
                    }
                )
            except (KeyError, ValueError) as e:
                logger.warning(f"[Position] 데이터 가공 오류: {e} - {item}")

        return positions
