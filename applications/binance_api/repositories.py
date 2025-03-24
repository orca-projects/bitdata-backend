from binance.client import Client


class BinanceApiRepository:
    @staticmethod
    def is_connected(api_key, secret_key):
        try:
            client = Client(api_key, secret_key)
            client.get_account()

            return True
        except Exception as e:
            print(f"Binance API 연결 실패: {e}")
            return False

    @staticmethod
    def get_binance_uid(api_key, secret_key):
        try:
            client = Client(api_key, secret_key)
            account_info = client.get_account()
            uid = account_info.get("uid")

            return uid
        except Exception as e:
            print(f"Binance UID 조회 중 오류 발생: {e}")
            return None

    # 25.02.13 윤택한 생성
    # Binance All Orders API 호출
    @staticmethod
    def fetch_orders_data(api_key, secret_key):
        try:
            client = Client(api_key, secret_key)
            # Binance 선물 API - Orders 조회
            response = client.futures_get_all_orders(orderId=0, limit=1000)
            # Orders Data 반환
            return response

        except Exception as e:
            print(f"Binance All Orders 조회 중 오류 발생: {e}")
            return None

    # 25.02.13 윤택한 생성
    # Binance Account Trade List API 호출
    @staticmethod
    def fetch_trades_data(api_key, secret_key):
        try:
            client = Client(api_key, secret_key)
            # Binance 선물 API - Trades 조회
            response = client.futures_account_trades(fromId=0, limit=1000)
            # Trades Data 반환
            return response

        except Exception as e:
            print(f"Binance Trade List 조회 중 오류 발생: {e}")
            return None

    # 25.02.12 윤택한 생성
    # Binance Get Income History API 호출
    @staticmethod
    def fetch_income_history_data(api_key, secret_key, start_time):
        try:
            client = Client(api_key, secret_key)
            # Binance 선물 API - Transactions 조회
            response = client.futures_income_history(startTime=start_time, limit=1000)
            # Transactions Data 반환
            return response

        except Exception as e:
            print(f"Binance Transaction List 조회 중 오류 발생: {e}")
            return None

    # 25.02.24 윤택한 생성
    # Binance Position Information API 호출
    @staticmethod
    def fetch_position_info_data(api_key, secret_key):
        try:
            client = Client(api_key, secret_key)
            # Binance 선물 API - Position Info 조회
            response = client.futures_position_information()
            # Position Info 반환
            return response
        except Exception as e:
            print(f"Binanace Position Information 조회 중 오류 발생: {e}")
            return None
