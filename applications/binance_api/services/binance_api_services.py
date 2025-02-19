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
        
        # all_order = BinanceApiRepository.fetch_all_orders(api_key, secret_key)
        # trade_list = BinanceApiRepository.fetch_trades_history(api_key, secret_key)
        # transaction = BinanceApiRepository.fetch_income_history(api_key, secret_key)

        return uid
    
    @staticmethod
    def get_orders_data(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        all_order = BinanceApiRepository.fetch_orders_data(api_key, secret_key)

        return all_order
    
    @staticmethod
    def get_trades_data(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]
    
        trades_data = BinanceApiRepository.fetch_trades_data(api_key, secret_key)

        return trades_data
    
    @staticmethod
    def get_transactions_data(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        transactions_data = BinanceApiRepository.fetch_income_history_data(api_key, secret_key)

        return transactions_data

