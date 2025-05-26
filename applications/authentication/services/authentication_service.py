from applications.users.repositories import UserRepository


class AuthenticationService:
    @staticmethod
    def login(request, kakao_uid: int) -> bool:
        user = UserRepository.get_user_by_kakao_uid(kakao_uid)

        if not user:
            return False

        request.session["is_login"] = True

        return True

    @staticmethod
    def logout(request):
        request.session.flush()
