from django.urls import path
from applications.users.views import BinanceKey

urlpatterns = [path("binance-key/", BinanceKey.as_view(), name="binance-key")]
