from django.urls import path
from applications.transaction.views import (
    Transaction,
)

urlpatterns = [
    path("", Transaction.as_view(), name="transaction"),
]
