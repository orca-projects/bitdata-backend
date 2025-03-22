from datetime import datetime, timezone

from applications.users.repositories import UserKeyInfoRepository
from applications.transaction.repositories import OrdersRepository
from applications.transaction.repositories import TradesRepository
from applications.transaction.repositories import TransactionsRepository

from applications.binance_api.services import BinanceApiServices


class CollectServices:
    @staticmethod
    def collect(kakao_id, binance_api_key):
        is_connected = BinanceApiServices.is_connected(binance_api_key)
        CollectServices.save_is_connected(kakao_id, is_connected)

        if not is_connected:
            return  # 연결되지 않으면 종료

        binance_id = BinanceApiServices.get_binance_id(binance_api_key)
        orders_data = BinanceApiServices.get_orders_data(binance_api_key)
        trades_data = BinanceApiServices.get_trades_data(binance_api_key)
        transactions_data = BinanceApiServices.get_transactions_data(binance_api_key)

        CollectServices.save_binance_id(kakao_id, binance_id)
        CollectServices.save_orders_data(binance_id, orders_data)
        CollectServices.save_trades_data(binance_id, trades_data)
        CollectServices.save_transactions_data(binance_id, transactions_data)

    @staticmethod
    def save_is_connected(kakao_id, is_connected):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        UserKeyInfoRepository.update(active_user_key_info, is_connected=is_connected)

    @staticmethod
    def save_binance_id(kakao_id, binance_id):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        UserKeyInfoRepository.update(active_user_key_info, binance_id=binance_id)

    @staticmethod
    def save_orders_data(binance_id, orders_data):
        OrdersRepository.create(binance_id, orders_data=orders_data)

    @staticmethod
    def save_trades_data(binance_id, trades_data):
        TradesRepository.create(binance_id, trades_data=trades_data)

    @staticmethod
    def save_transactions_data(binance_id, transactions_data):
        TransactionsRepository.create(binance_id, transactions_data=transactions_data)

    @staticmethod
    def save_last_collected(kakao_id):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        UserKeyInfoRepository.update(
            active_user_key_info, last_collected=datetime.now(timezone.utc)
        )
