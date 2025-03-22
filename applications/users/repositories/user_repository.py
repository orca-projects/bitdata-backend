import logging

from applications.users.models.user import User


logger = logging.getLogger(__name__)


class UserRepository:
    @staticmethod
    def find_by_kakao_id(kakao_id):
        user_kakao = User.objects.filter(kakao_id=kakao_id, deleted_at=None).first()
        return user_kakao

    @staticmethod
    def create(user_info):
        try:
            User.objects.create(
                kakao_id=user_info.get("kakao_id"),
                name=user_info.get("name"),
                phone_number=user_info.get("phone_number"),
                account_email=user_info.get("email"),
            )
        except Exception as e:
            raise e
