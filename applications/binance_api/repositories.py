from binance.client import Client

from core.exceptions import NullException


class BinanceUidRepository:
    @staticmethod
    def get(api_key, secret_key):
        try:
            client = Client(api_key, secret_key)
            account_info = client.get_account()
            uid = account_info.get("uid")
            
            if uid is None:
                raise NullException("uid")

            return uid
        except NullException as e:
            raise e
        except Exception as e:
            raise RuntimeError(f"Binance UID 조회 중 오류 발생: {e}")