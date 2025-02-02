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
