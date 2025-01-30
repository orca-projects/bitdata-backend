from django.urls import path
from applications.users.views import BinanceKey, Collect

urlpatterns = [
    path("binance-key/", BinanceKey.as_view(), name="binance-key"),
    path("collect/", Collect.as_view(), name="collect"),
]
