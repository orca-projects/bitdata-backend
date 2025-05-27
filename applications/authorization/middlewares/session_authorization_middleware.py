from django.http import JsonResponse


class SessionAuthorizationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_paths = {
            "/api/authn/login",
            "/api/authn/join",
            "/api/authz/check",
        }

    def __call__(self, request):
        path = request.path_info

        if not any(path.startswith(p) for p in self.exempt_paths):
            if not request.session.get("is_login"):
                return JsonResponse({"detail": "unauthenticated"}, status=401)

        return self.get_response(request)
