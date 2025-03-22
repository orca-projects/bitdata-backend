from applications.users.repositories import (
    UserRepository,
    UserKeyInfoRepository,
)


class ProfileServices:
    @staticmethod
    def get_profile(kakao_id):
        try:
            user_kakao = UserRepository.find_by_kakao_id(kakao_id)
            username = user_kakao.name

            active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(
                kakao_id
            )
            is_connected = active_user_key_info.is_connected
            api_key = active_user_key_info.binance_api_key
            binance_uid = active_user_key_info.binance_id

            username_masked = ProfileServices.mask_username(username)
            api_key_masked = ProfileServices.mask_api_key(api_key)

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
