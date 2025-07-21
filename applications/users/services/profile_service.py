from applications.users.repositories import (
    UserRepository,
    UserApiKeyRepository,
    UserBinanceRepository,
)


class ProfileService:
    @staticmethod
    def get_profile(kakao_uid):
        try:
            profile = {
                "username": "",
                "is_connected": False,
                "api_key": None,
                "binance_uid": None,
            }

            user = UserRepository.get_user_by_kakao_uid(kakao_uid)
            if not user:
                return profile

            profile["username"] = ProfileService.mask_username(user.name)

            active_user_api_key = UserApiKeyRepository.get_active_by_user_id(user.id)
            if active_user_api_key:
                profile["is_connected"] = active_user_api_key.is_connected
                api_key = active_user_api_key.binance_api_key
                profile["api_key"] = ProfileService.mask_api_key(api_key)

                binance_uid = UserBinanceRepository.get_binance_uid_by_id(
                    active_user_api_key.user_binance_id
                )
                profile["binance_uid"] = binance_uid

            return profile

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
