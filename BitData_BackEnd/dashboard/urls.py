from django.urls import path
# from .views import account_info_view
from dashboard.views import GetBinanceTradeData

# from auths.views import 
urlpatterns = [
    path('getbinancedata/', GetBinanceTradeData.as_view(), name='dashboard-get-binance-data')
]