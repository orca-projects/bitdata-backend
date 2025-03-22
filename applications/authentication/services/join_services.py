class JoinServices:
    @staticmethod
    def get_user_info(request):
        user_info = request.session.get("user_info")

        if not user_info:
            raise ValueError("User info not found in session")

        return user_info
