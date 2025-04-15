import logging

from applications.users.models.user_model import User


logger = logging.getLogger(__name__)


class UserRepository:
    @staticmethod
    def get_user_id_by_kakao_uid(kakao_uid: int) -> int | None:
        user = User.objects.filter(kakao_uid=kakao_uid, deleted_at=None).first()
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
