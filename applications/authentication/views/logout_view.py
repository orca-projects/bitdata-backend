from django.http import JsonResponse
from rest_framework.views import APIView
from core.utils.response_util import ResponseUtil

from applications.authentication.services import AuthenticationService


class Logout(APIView):
    def get(self, request) -> JsonResponse:
        AuthenticationService.logout(request)
        return ResponseUtil.success(data={"result": True})
