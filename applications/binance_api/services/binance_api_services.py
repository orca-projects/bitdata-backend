from applications.binance_api.repositories import BinanceUidRepository
from applications.users.models import UserKeyInfo


class BinanceApiServices:
    @staticmethod
    def get_uid(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        uid = BinanceUidRepository.get(api_key, secret_key)

        return uid
