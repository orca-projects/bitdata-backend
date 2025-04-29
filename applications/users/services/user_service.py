from applications.users.repositories import UserRepository


class UserService:
    @staticmethod
    def is_member(kakao_uid):
        user_id = UserRepository.get_user_id_by_kakao_uid(kakao_uid)
        return user_id is not None
