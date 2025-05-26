from django.http import JsonResponse
from rest_framework.views import APIView


class Check(APIView):
    def get(self, request) -> JsonResponse:
        return JsonResponse({"state": "ALLOWED"})
