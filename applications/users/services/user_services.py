from applications.users.repositories import UserRepository


class UserServices:
    @staticmethod
    def is_member(kakao_id):
        user_kakao = UserRepository.find_by_kakao_id(kakao_id)
        return user_kakao is not None
