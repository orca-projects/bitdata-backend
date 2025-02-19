import logging

from applications.users.models import User


logger = logging.getLogger(__name__)


class UserRepository:
    @staticmethod
    def find_by_kakao_id(kakao_id):
        user_kakao = User.objects.filter(
            kakao_id=kakao_id, deleted_at=None
        ).first()
        return user_kakao
