import logging
from django.utils import timezone

from applications.authentication.services import AuthenticationService
from applications.users.repositories import UserRepository

logger = logging.getLogger(__name__)


class UserService:
    @staticmethod
    def get_user(kakao_uid):
        user = UserRepository.get_user_by_kakao_uid(kakao_uid)
        return user

    @staticmethod
    def is_member(kakao_uid):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)
        return user_id is not None

    @staticmethod
    def join(user_data):
        UserRepository.set_user(user_data)

    @staticmethod
    def withdraw(request, kakao_uid, reason):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)
        if user_id is None:
            logger.warning(f"kakao_uid invalid: {kakao_uid}")
            return False

        update_data = {
            "account_email": None,
            "name": None,
            "phone_number": None,
            "updated_at": timezone.now(),
            "is_deleted": True,
            "withdraw_reason": reason.strip(),
        }

        result = UserRepository.update_user_by_user_id(user_id, update_data)

        if not result:
            logger.warning("UserService/withdraw is failed")

        AuthenticationService.logout(request)

        return result
