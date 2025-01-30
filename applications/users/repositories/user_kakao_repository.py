import logging

from applications.users.models import UserKakao


logger = logging.getLogger(__name__)


class UserKakaoRepository:
    @staticmethod
    def find_by_kakao_id(kakao_id):
        user_kakao = UserKakao.objects.filter(
            kakao_id=kakao_id, deleted_at=None
        ).first()
        return user_kakao
