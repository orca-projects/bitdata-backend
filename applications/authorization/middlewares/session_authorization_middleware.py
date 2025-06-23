import re
from django.http import JsonResponse


class SessionAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        self.kakao_authentication_patterns = [
            r"^/api/authz/kakao(?:/.*)?$",
        ]

        self.login_patterns = [
            r"^/api/authz/login(?:/.*)?$",
        ]

    def _match_any(self, patterns, path):
        return any(re.match(pattern, path) for pattern in patterns)

    def __call__(self, request):
        path = request.path_info

        if self._match_any(self.kakao_authentication_patterns, path):
            return self._check_kakao_authenticated(request)

        if self._match_any(self.login_patterns, path):
            return self._check_login(request)

        return self.get_response(request)

    def _check_kakao_authenticated(self, request):
        if not request.session.get("is_kakao_authenticated", False):
            return JsonResponse({"state": "UNAUTHORIZED"}, status=401)
        return self.get_response(request)

    def _check_login(self, request):
        if not request.session.get("is_login", False):
            return JsonResponse({"state": "UNAUTHORIZED"}, status=401)
        return self.get_response(request)
