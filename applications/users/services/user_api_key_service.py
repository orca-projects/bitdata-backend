from applications.users.repositories import UserApiKeyRepository


class UserApiKeyService:
    @staticmethod
    def has_binance_api_key(kakao_uid):
        user_api_key = UserApiKeyRepository.find_active_by_kakao_uid(kakao_uid)
        return user_api_key is not None

    @staticmethod
    def save_binance_api_key(kakao_uid, binance_api_key):
        UserApiKeyService.deactivate_active_user_api_key(kakao_uid)

        UserApiKeyRepository.create(kakao_uid, binance_api_key)

    @staticmethod
    def deactivate_active_user_api_key(kakao_uid):
        active_user_api_key = UserApiKeyRepository.find_active_by_kakao_uid(kakao_uid)
        if active_user_api_key:
            UserApiKeyRepository.update(active_user_api_key, is_key_active=False)

    @staticmethod
    def get_binance_api_key(kakao_uid):
        user_api_key = UserApiKeyRepository.find_active_by_kakao_uid(kakao_uid)

        binance_api_key = {
            "api_key": user_api_key.binance_api_key,
            "secret_key": user_api_key.binance_secret_key,
        }
        return binance_api_key

    @staticmethod
    def get_binance_id(kakao_uid):
        user_api_key = UserApiKeyRepository.find_active_by_kakao_uid(kakao_uid)
        return user_api_key.binance_id
