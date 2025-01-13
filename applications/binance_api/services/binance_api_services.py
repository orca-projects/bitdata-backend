from applications.binance_api.repositories import BinanceUidRepository
from applications.users.models import UserKeyInfo


class BinanceApiServices:
    @staticmethod
    def get_uid(binance_api_key):
        api_key = binance_api_key["api_key"]
        secret_key = binance_api_key["secret_key"]

        uid = BinanceUidRepository.get(api_key, secret_key)
        
        return uid

    @staticmethod
    def save_uid(kakao_id, uid):
        try:
            user_key_info, created = UserKeyInfo.objects.update_or_create(
                kakao_id=kakao_id, defaults={"binance_id": uid}
            )
        except Exception as e:
            raise RuntimeError(f"바이낸스 UID 저장 중 오류가 발생했습니다: {e}")
