from datetime import datetime, timezone

from applications.users.repositories import UserApiKeyRepository
from applications.transaction.repositories import OrderHistoryRepository
from applications.transaction.repositories import TradeHistoryRepository
from applications.transaction.repositories import TransactionHistoryRepository

from applications.binance_api.services import BinanceApiServices


class CollectService:
    @staticmethod
    def collect(kakao_uid, binance_api_key):
        is_connected = BinanceApiServices.is_connected(binance_api_key)
        CollectService.save_is_connected(kakao_uid, is_connected)

        if not is_connected:
            return  # 연결되지 않으면 종료

        binance_id = BinanceApiServices.get_binance_id(binance_api_key)
        orders_data = BinanceApiServices.get_orders_data(binance_api_key)
        trades_data = BinanceApiServices.get_trades_data(binance_api_key)
        transactions_data = BinanceApiServices.get_transactions_data(binance_api_key)

        CollectService.save_binance_id(kakao_uid, binance_id)
        CollectService.save_orders_data(binance_id, orders_data)
        CollectService.save_trades_data(binance_id, trades_data)
        CollectService.save_transactions_data(binance_id, transactions_data)

    @staticmethod
    def save_is_connected(kakao_uid, is_connected):
        active_user_api_key = UserApiKeyRepository.find_active_by_kakao_uid(kakao_uid)
        UserApiKeyRepository.update(active_user_api_key, is_connected=is_connected)

    @staticmethod
    def save_binance_id(kakao_uid, binance_id):
        active_user_api_key = UserApiKeyRepository.find_active_by_kakao_uid(kakao_uid)
        UserApiKeyRepository.update(active_user_api_key, binance_id=binance_id)

    @staticmethod
    def save_orders_data(binance_id, orders_data):
        OrderHistoryRepository.create(binance_id, orders_data=orders_data)

    @staticmethod
    def save_trades_data(binance_id, trades_data):
        TradeHistoryRepository.create(binance_id, trades_data=trades_data)

    @staticmethod
    def save_transactions_data(binance_id, transactions_data):
        TransactionHistoryRepository.create(
            binance_id, transactions_data=transactions_data
        )

    @staticmethod
    def save_last_collected(kakao_uid):
        active_user_api_key = UserApiKeyRepository.find_active_by_kakao_uid(kakao_uid)
        UserApiKeyRepository.update(
            active_user_api_key, last_collected=datetime.now(timezone.utc)
        )
