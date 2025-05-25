from django.urls import path
from applications.users.views import (
    BinanceKey,
    Collect,
    Profile,
    Withdraw,
)

urlpatterns = [
    path("binance-key/", BinanceKey.as_view(), name="binance-key"),
    path("collect/", Collect.as_view(), name="collect"),
    path("profile/", Profile.as_view(), name="profile"),
    path("withdraw/", Withdraw.as_view(), name="withdraw"),
]
