class JoinService:
    @staticmethod
    def get_user_data(request):
        user_data = request.session.get("user_data")

        if not user_data:
            raise ValueError("User data not found in session")

        return user_data
