from django.utils import timezone

from applications.users.repositories import (
    UserRepository,
    UserApiKeyRepository,
    UserBinanceRepository,
)
from applications.transaction.repositories import OrderHistoryRepository
from applications.transaction.repositories import TradeHistoryRepository
from applications.transaction.repositories import TransactionHistoryRepository
from applications.binance_api.services import BinanceApiServices


class CollectService:
    @staticmethod
    def collect(kakao_uid, binance_api_key):
        is_connected = BinanceApiServices.is_connected(binance_api_key)

        if not is_connected:
            return

        binance_uid = BinanceApiServices.get_binance_uid(binance_api_key)
        orders_data = BinanceApiServices.get_orders_data(binance_api_key)
        trades_data = BinanceApiServices.get_trades_data(binance_api_key)
        transactions_data = BinanceApiServices.get_transactions_data(
            binance_uid, binance_api_key
        )

        CollectService.save_is_connected(kakao_uid, is_connected)
        CollectService.save_binance_uid(kakao_uid, binance_uid)
        CollectService.save_orders_data(binance_uid, orders_data)
        CollectService.save_trades_data(binance_uid, trades_data)
        CollectService.save_transactions_data(binance_uid, transactions_data)

    @staticmethod
    def save_is_connected(kakao_uid, is_connected):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)
        active_user_api_key = UserApiKeyRepository.get_active_by_user_id(user_id)
        UserApiKeyRepository.update_user_api_key(
            active_user_api_key, is_connected=is_connected
        )

    @staticmethod
    def save_binance_uid(kakao_uid, binance_uid):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)
        active_user_api_key = UserApiKeyRepository.get_active_by_user_id(user_id)
        user_binance = UserBinanceRepository.set_user_binance(binance_uid)
        UserApiKeyRepository.update_user_api_key(
            active_user_api_key, user_binance_id=user_binance.id
        )

    @staticmethod
    def save_orders_data(binance_uid, orders_data):
        OrderHistoryRepository.set_order_history(binance_uid, orders_data=orders_data)

    @staticmethod
    def save_trades_data(binance_uid, trades_data):
        TradeHistoryRepository.set_trade_history(binance_uid, trades_data=trades_data)

    @staticmethod
    def save_transactions_data(binance_uid, transactions_data):
        TransactionHistoryRepository.set_transaction_history(
            binance_uid, transactions_data=transactions_data
        )

    @staticmethod
    def save_last_collected(kakao_uid):
        active_user_api_key = UserApiKeyRepository.get_active_by_user_id(kakao_uid)
        UserApiKeyRepository.update_user_api_key(
            active_user_api_key, last_collected=timezone.now()
        )
