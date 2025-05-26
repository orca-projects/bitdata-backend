from django.http import JsonResponse


class SessionAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = {
            "/api/authn/login",
            "/api/authn/join",
            "/api/authz/check",
            "/api/user/binance-key",
        }

    def __call__(self, request):
        path = request.path_info

        if any(path.startswith(p) for p in self.exempt_paths):
            return self.get_response(request)

        if not request.session.get("is_login"):
            return JsonResponse({"state": "UNAUTHORIZED"}, status=401)

        if not request.session.get("has_api_key"):
            return JsonResponse({"state": "NEED_API_KEY"}, status=401)

        return self.get_response(request)
