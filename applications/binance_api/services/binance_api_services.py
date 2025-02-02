from applications.binance_api.repositories import BinanceApiRepository


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
