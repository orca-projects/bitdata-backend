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
                kakaoId=user_info.get("kakao_id"),
                name=user_info.get("name"),
                phoneNumber=user_info.get("phone_number"),
                accountEmail=user_info.get("email"),
            )
        except Exception as e:
            raise e
