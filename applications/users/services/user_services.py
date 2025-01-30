from applications.users.models import UserKakao, UserKeyInfo


class UserServices:
    @staticmethod
    def is_member(user_info):
        try:
            exists = UserKakao.objects.filter(
                kakao_id=user_info["kakao_id"],
                account_email=user_info["email"],
                phone_number=user_info["phone_number"],
                name=user_info["name"],
            ).exists()
            return exists
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return False

    @staticmethod
    def has_binance_key(kakao_id):
        try:
            exists = (
                UserKeyInfo.objects.filter(
                    kakao_id=kakao_id,
                )
                .exclude(binance_api_key__isnull=True)
                .exclude(binance_secret_key__isnull=True)
                .exists()
            )
            return exists
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return False

    @staticmethod
    def get_kakao_id(user_info):
        try:
            kakao_id = user_info["kakao_id"]

            user_kakao = UserKakao.objects.get(kakao_id=kakao_id)

            return user_kakao.kakao_id
        except UserKakao.DoesNotExist:
            # 카카오 ID가 없으면 예외 처리
            print(f"카카오 ID '{kakao_id}'에 해당하는 사용자 정보가 없습니다.")
            return None
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return None

    @staticmethod
    def save_binance_api_key(kakao_id, binance_api_key):
        try:
            user_key_info, created = UserKeyInfo.objects.update_or_create(
                kakao_id=kakao_id,
                defaults={
                    "binance_api_key": binance_api_key["api_key"],
                    "binance_secret_key": binance_api_key["secret_key"],
                },
            )
        except Exception as e:
            raise RuntimeError(f"바이낸스 키 저장 중 오류가 발생했습니다: {e}")

    @staticmethod
    def get_binance_api_key(kakao_id):
        try:
            user_key_info = UserKeyInfo.objects.get(kakao_id=kakao_id)

            binance_api_key = user_key_info.binance_api_key
            binance_secret_key = user_key_info.binance_secret_key

            return {
                "api_key": binance_api_key,
                "secret_key": binance_secret_key,
            }
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return None

    @staticmethod
    def save_binance_uid(kakao_id, uid):
        try:
            user_key_info, created = UserKeyInfo.objects.update_or_create(
                kakao_id=kakao_id, defaults={"binance_id": uid}
            )
        except Exception as e:
            raise RuntimeError(f"바이낸스 UID 저장 중 오류가 발생했습니다: {e}")

    @staticmethod
    def get_profile(kakao_id):
        try:
            user_kakao = UserKakao.objects.get(kakao_id=kakao_id)
            username = user_kakao.name

            user_key_info = UserKeyInfo.objects.get(kakao_id=kakao_id)
            binance_api_key = user_key_info.binance_api_key
            binance_uid = user_key_info.binance_id

            username_masked = UserServices.mask_username(username)
            api_key_masked = binance_api_key[0] + "****" + binance_api_key[-1]
            secret_key_masked = "*" * 8

            return {
                "username": username_masked,
                "api_key": api_key_masked,
                "secret_key": secret_key_masked,
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
