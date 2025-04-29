import logging

from applications.users.models import UserApiKey


logger = logging.getLogger(__name__)


class UserApiKeyRepository:
    @staticmethod
    def find_by_id(id):
        try:
            user_api_key = UserApiKey.objects.get(id=id)
            return user_api_key
        except UserApiKey.DoesNotExist:
            logger.warning(f"UserApiKey with id {id} not found.")
            return None
        except Exception as e:
            logger.error(f"find_by_id error: {e}", exc_info=True)
            raise RuntimeError("데이터베이스 조회 중 오류 발생")

    @staticmethod
    def get_active_by_user_id(user_id):
        user_api_key = UserApiKey.objects.filter(
            user_id=user_id, is_key_active=True
        ).first()
        return user_api_key

    # 25.02.27(목) 윤택한
    # Last Collected 값이 있으면 해당 값을 없으면 None을 반환
    @staticmethod
    def get_last_collected(binance_uid):
        last_collected = (
            UserApiKey.objects.filter(binance_uid=binance_uid)
            .order_by("-last_collected")
            .values_list("last_collected", flat=True)
            .first()
        )
        return last_collected if last_collected else None

    @staticmethod
    def set_user_api_key(user_id, binance_api_key):
        try:
            user_api_key = UserApiKey.objects.create(
                user_id=user_id,
                binance_api_key=binance_api_key.get("api_key"),
                binance_secret_key=binance_api_key.get("secret_key"),
            )
            return user_api_key
        except Exception as e:
            logger.error(f"Binance API 키 생성 중 오류 발생: {e}", exc_info=True)
            raise RuntimeError("Binance API 키 생성 중 오류 발생")

    @staticmethod
    def update_user_api_key(user_api_key, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(user_api_key, key, value)
            user_api_key.save()
            return user_api_key
        except Exception as e:
            logger.error(f"UserApiKey 업데이트 중 오류 발생: {e}", exc_info=True)
            raise RuntimeError("UserApiKey 업데이트 중 오류 발생")
