from applications.users.repositories import UserKeyInfoRepository


class UserKeyInfoServices:
    @staticmethod
    def has_binance_api_key(kakao_id):
        user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        return user_key_info is not None

    @staticmethod
    def save_binance_api_key(kakao_id, binance_api_key):
        UserKeyInfoServices.deactivate_active_user_key_info(kakao_id)

        UserKeyInfoRepository.create(kakao_id, binance_api_key)

    @staticmethod
    def deactivate_active_user_key_info(kakao_id):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        if active_user_key_info:
            UserKeyInfoRepository.update(active_user_key_info, is_key_active=False)

    @staticmethod
    def get_binance_api_key(kakao_id):
        user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)

        binance_api_key = {
            "api_key": user_key_info.binance_api_key,
            "secret_key": user_key_info.binance_secret_key,
        }
        return binance_api_key

    @staticmethod
    def get_binance_id(kakao_id):
        user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        return user_key_info.binance_id
