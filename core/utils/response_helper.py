from django.http import JsonResponse


class ResponseHelper:
    @staticmethod
    def create(request=None, data=None, message="success", status=200, error=None):
        response = {"message": message}

        if data:
            response.update(data)

        if request and hasattr(request, "session"):
            request.session.save()
            response["session_key"] = request.session.session_key

        if error:
            response["error"] = error

        return JsonResponse(response, status=status)

    @staticmethod
    def success(request=None, data=None, message="success"):
        return ResponseHelper.create(
            request=request, data=data, message=message, status=200
        )

    @staticmethod
    def error(request=None, message="error", error_details=None, status=500):
        return ResponseHelper.create(
            request=request,
            data=None,
            message=message,
            status=status,
            error=error_details,
        )
