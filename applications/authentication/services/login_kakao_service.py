import requests

from rest_framework.exceptions import AuthenticationFailed

from urllib.parse import urlencode
from django.conf import settings


class KakaoService:
    @staticmethod
    def get_login_url(state):
        base_url = "https://kauth.kakao.com/oauth/authorize"
        params = {
            "response_type": settings.KAKAO_REPONSE_TYPE,
            "redirect_uri": settings.KAKAO_REDIRECT_URL,
            "state": state,
            "client_id": settings.KAKAO_REST_API_KEY,
            "scope": "",
            "through_account": "true",
        }
        return f"{base_url}?{urlencode(params)}"

    @staticmethod
    def validate_sate(session_state, request_state):
        if session_state != request_state:
            raise AuthenticationFailed("State 값이 일치하지 않습니다.")

    @staticmethod
    def get_access_token(code):
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.KAKAO_REST_API_KEY,
            "redirect_uri": settings.KAKAO_REDIRECT_URL,
            "client_secret": settings.KAKAO_CLIENT_SECRET,
            "code": code,
        }
        headers = {"Content-type": "application/x-www-form-urlencoded;charset=utf-8"}

        access_token_response = requests.post(
            "https://kauth.kakao.com/oauth/token", data=data, headers=headers
        )

        access_token = access_token_response.json().get("access_token")
        return access_token

    @staticmethod
    def validate_access_token(access_token):
        headers = {"Authorization": f"Bearer {access_token}"}

        token_validate_response = requests.get(
            "https://kapi.kakao.com/v1/user/access_token_info", headers=headers
        )

        if token_validate_response.status_code != 200:
            raise AuthenticationFailed("토큰 검증에 실패했습니다.")

    @staticmethod
    def get_user_data(access_token):
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        }

        user_data_response = requests.post(
            "https://kapi.kakao.com/v2/user/me", headers=headers
        )

        user_data_json = user_data_response.json()

        user_data = {
            "kakao_uid": user_data_json.get("id"),
            "name": user_data_json.get("kakao_account", {}).get("name"),
            "phone_number": user_data_json.get("kakao_account", {}).get("phone_number"),
            "email": user_data_json.get("kakao_account", {}).get("email"),
        }

        return user_data

    @staticmethod
    def validate_user_data(user_data):
        missing_fields = [key for key, value in user_data.items() if not value]
        if missing_fields:
            raise AuthenticationFailed(
                f"필요한 사용자 정보가 누락되었습니다: {', '.join(missing_fields)}"
            )

    @staticmethod
    def save_session_user_data(request, user_data):
        request.session["user_data"] = user_data
