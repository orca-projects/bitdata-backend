import logging

from applications.users.models import User


logger = logging.getLogger(__name__)


class UserRepository:
    @staticmethod
    def get_user_by_kakao_uid(kakao_uid: int) -> User | None:
        user = User.objects.filter(kakao_uid=kakao_uid, is_deleted=False).first()
        return user

    @staticmethod
    def get_user_id_by_kakao_uid(kakao_uid: int) -> int | None:
        user = User.objects.filter(kakao_uid=kakao_uid, is_deleted=False).first()
        return user.id if user else None

    @staticmethod
    def set_user(user_data):
        try:
            User.objects.create(
                kakao_uid=user_data.get("kakao_uid"),
                name=user_data.get("name"),
                phone_number=user_data.get("phone_number"),
                account_email=user_data.get("email"),
            )
        except Exception as e:
            raise e

    @staticmethod
    def update_user_by_user_id(user_id: int, data: dict) -> bool:
        try:
            updated_count = User.objects.filter(id=user_id).update(**data)
            return updated_count > 0
        except Exception as e:
            logger.error(f"Failed to update user {user_id}: {e}")
            return False
