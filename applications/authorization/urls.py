from django.urls import path
from applications.authorization.views import (
    Check,
)

urlpatterns = [
    path("", Check.as_view(), name="check"),
]
