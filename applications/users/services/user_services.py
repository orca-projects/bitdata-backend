from applications.users.repositories import UserKakaoRepository, UserKeyInfoRepository


class UserServices:
    @staticmethod
    def is_member(kakao_id):
        user_kakao = UserKakaoRepository.find_by_kakao_id(kakao_id)
        return user_kakao is not None

    @staticmethod
    def has_binance_api_key(kakao_id):
        user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        return user_key_info is not None

    @staticmethod
    def save_binance_api_key(kakao_id, binance_api_key):
        UserServices.deactivate_active_user_key_info(kakao_id)

        UserKeyInfoRepository.create_user_key_info(kakao_id, binance_api_key)

    @staticmethod
    def deactivate_active_user_key_info(kakao_id):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        if active_user_key_info:
            UserKeyInfoRepository.update_user_key_info(
                active_user_key_info, is_key_active=False
            )

    @staticmethod
    def get_binance_api_key(kakao_id):
        user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)

        binance_api_key = {
            "api_key": user_key_info.binance_api_key,
            "secret_key": user_key_info.binance_secret_key,
        }
        return binance_api_key

    @staticmethod
    def save_is_connected(kakao_id, is_connected):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        UserKeyInfoRepository.update_user_key_info(
            active_user_key_info, is_connected=is_connected
        )

    @staticmethod
    def save_binance_id(kakao_id, binance_id):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        UserKeyInfoRepository.update_user_key_info(
            active_user_key_info, binance_id=binance_id
        )

    @staticmethod
    def get_profile(kakao_id):
        try:
            user_kakao = UserKakaoRepository.find_by_kakao_id(kakao_id)
            username = user_kakao.name

            active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(
                kakao_id
            )
            is_connected = active_user_key_info.is_connected
            api_key = active_user_key_info.binance_api_key
            binance_uid = active_user_key_info.binance_id

            username_masked = UserServices.mask_username(username)
            api_key_masked = UserServices.mask_api_key(api_key)

            return {
                "username": username_masked,
                "is_connected": is_connected,
                "api_key": api_key_masked,
                "binance_uid": binance_uid,
            }
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return None

    @staticmethod
    def mask_username(username):
        if len(username) == 1:
            return "*"
        elif len(username) == 2:
            return f"{username[0]}*"
        elif len(username) == 3:
            return f"{username[0]}*{username[2]}"
        else:
            return f"{username[0]}{'*' * (len(username) - 2)}{username[-1]}"

    @staticmethod
    def mask_api_key(api_key):
        return api_key[0] + "****" + api_key[-1]
