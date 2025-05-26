from django.urls import path
from applications.authorization.views import (
    Check,
)

urlpatterns = [
    path("", Check.as_view(), name="check"),
    path("kakao/", Check.as_view(), name="check-kakao-login"),
    path("login/", Check.as_view(), name="check-login"),
    path("api-key/", Check.as_view(), name="check-api-key"),
]
