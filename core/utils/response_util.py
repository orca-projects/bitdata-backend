from django.http import JsonResponse


class ResponseUtil:
    @staticmethod
    def create(state=None, message=None, data=None, status=200):
        response = {}

        if state:
            response["state"] = state

        if message:
            response["message"] = message

        if data:
            response.update(data)

        return JsonResponse(
            response,
            status=status,
            safe=False,
            json_dumps_params={"ensure_ascii": False},
        )

    @staticmethod
    def success(data=None, message=None):
        return ResponseUtil.create(
            state="success",
            data=data,
            message=message,
            status=200,
        )

    @staticmethod
    def error(data=None, message="예상치 못한 오류"):
        return ResponseUtil.create(
            state="error",
            data=data,
            message=message,
            status=200,
        )
