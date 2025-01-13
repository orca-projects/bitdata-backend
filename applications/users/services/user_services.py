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

            return user_kakao
        except UserKakao.DoesNotExist:
            # 카카오 ID가 없으면 예외 처리
            print(f"카카오 ID '{kakao_id}'에 해당하는 사용자 정보가 없습니다.")
            return None
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return None

    @staticmethod
    def save_binance_key(kakao_id, binance_api_key):
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
            binance_api_key = UserKeyInfo.objects.get(kakao_id=kakao_id).binance_api_key
            binance_secret_key = UserKeyInfo.objects.get(
                kakao_id=kakao_id
            ).binance_secret_key

            return {
                "api_key": binance_api_key,
                "secret_key": binance_secret_key,
            }
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return None
