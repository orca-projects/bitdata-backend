from django.urls import path
from applications.binance_api.views import Collect

urlpatterns = [
    path("collect/", Collect.as_view(), name="collect"),
]
