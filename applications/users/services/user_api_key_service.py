from applications.users.repositories import (
    UserRepository,
    UserApiKeyRepository,
    UserBinanceRepository,
)


class UserApiKeyService:
    @staticmethod
    def has_binance_api_key(kakao_uid):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)
        user_api_key = UserApiKeyRepository.get_active_by_user_id(user_id)
        return user_api_key is not None

    @staticmethod
    def save_binance_api_key(kakao_uid, binance_api_key):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)

        UserApiKeyService.deactivate_active_user_api_key(user_id)

        UserApiKeyRepository.set_user_api_key(user_id, binance_api_key)

    @staticmethod
    def deactivate_active_user_api_key(user_id):
        active_user_api_key = UserApiKeyRepository.get_active_by_user_id(user_id)

        if active_user_api_key:
            UserApiKeyRepository.update_user_api_key(
                active_user_api_key, is_key_active=False
            )

    @staticmethod
    def get_binance_api_key(kakao_uid):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)
        user_api_key = UserApiKeyRepository.get_active_by_user_id(user_id)
        
        if not user_api_key:
            return None
        return {
            "api_key": user_api_key.binance_api_key,
            "secret_key": user_api_key.binance_secret_key,
        }

    @staticmethod
    def get_binance_uid(kakao_uid):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)
        user_api_key = UserApiKeyRepository.get_active_by_user_id(user_id)
        user_binance_uid = UserBinanceRepository.get_binance_uid_by_id(
            user_api_key.user_binance_id
        )
        return user_binance_uid
