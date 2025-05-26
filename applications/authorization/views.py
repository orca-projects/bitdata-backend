from django.http import JsonResponse
from rest_framework.views import APIView
from core.utils.response_util import ResponseUtil


class Check(APIView):
    def get(self, request) -> JsonResponse:
        is_login = request.session.get("is_login", False)
        return ResponseUtil.success(data={"result": is_login})
