import logging

from applications.users.models import (
    User,
    UserKeyInfo,
)


logger = logging.getLogger(__name__)


class UserKeyInfoRepository:
    @staticmethod
    def find_by_id(id):
        try:
            user_key_info = UserKeyInfo.objects.get(id=id)
            return user_key_info
        except UserKeyInfo.DoesNotExist:
            logger.warning(f"UserKeyInfo with id {id} not found.")
            return None
        except Exception as e:
            logger.error(f"find_by_id error: {e}", exc_info=True)
            raise RuntimeError("데이터베이스 조회 중 오류 발생")

    @staticmethod
    def find_active_by_kakao_id(kakao_id):
        user_key_info = UserKeyInfo.objects.filter(
            kakao_id=kakao_id, is_key_active=True
        ).first()
        return user_key_info

    # 25.02.27(목) 윤택한
    # Last Collected 값이 있으면 해당 값을 없으면 None을 반환
    @staticmethod
    def get_last_collected(binance_id):
        last_collected = (
            UserKeyInfo.objects.filter(binance_id=binance_id)
            .order_by("-last_collected")
            .values_list("last_collected", flat=True)
            .first()
        )
        return last_collected if last_collected else None

    @staticmethod
    def create(kakao_id, binance_api_key):
        try:
            user_kakao = User.objects.filter(kakao_id=kakao_id, deleted_at=None).first()

            api_key = binance_api_key.get("api_key")
            secret_key = binance_api_key.get("secret_key")

            user_key_info = UserKeyInfo.objects.create(
                kakao_id=user_kakao,
                binance_api_key=api_key,
                binance_secret_key=secret_key,
                is_key_active = True # managed=False로 인해 default 값이 DB에 반영되지 않으므로 True를 명시적으로 지정
            )
            return user_key_info
        except Exception as e:
            logger.error(f"Binance API 키 생성 중 오류 발생: {e}", exc_info=True)
            raise RuntimeError("Binance API 키 생성 중 오류 발생")

    @staticmethod
    def update(user_key_info, **kwargs):
        try:
            for key, value in kwargs.items():
                setattr(user_key_info, key, value)
            user_key_info.save()
            return user_key_info
        except Exception as e:
            logger.error(f"UserKeyInfo 업데이트 중 오류 발생: {e}", exc_info=True)
            raise RuntimeError("UserKeyInfo 업데이트 중 오류 발생")
        
    @staticmethod
    def deactivate_all_active_keys(kakao_id):
        try:
            UserKeyInfo.objects.filter(kakao_id=kakao_id, is_key_active = True).update(is_key_active = False)
        except Exception as e:
            logger.error(f"{kakao_id}의 기존 API키 비활성화 중 오류 발생: {e}")
            raise RuntimeError ("API키 비활성화 중 오류 발생")
