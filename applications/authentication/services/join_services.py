from applications.users.models import UserKakao


class JoinServices:
    @staticmethod
    def get_user_info(request):
        user_info = request.session.get("user_info")

        if not user_info:
            raise ValueError("User info not found in session")

        return user_info

    @staticmethod
    def save_user_info(user_info):
        try:
            UserKakao.objects.create(
                kakao_id=user_info.get("kakao_id"),
                name=user_info.get("name"),
                phone_number=user_info.get("phone_number"),
                account_email=user_info.get("email"),
            )
        except Exception as e:
            raise e
