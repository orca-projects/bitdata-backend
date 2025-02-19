from django.http import JsonResponse

from rest_framework.views import APIView

from core.utils import ResponseHelper

from applications.users.services import UserServices
from applications.binance_api.services import BinanceApiServices


class BinanceKey(APIView):
    def post(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = user_info["kakao_id"]
            binance_api_key = {
                "api_key": request.data.get("api_key"),
                "secret_key": request.data.get("secret_key"),
            }

            UserServices.save_binance_api_key(kakao_id, binance_api_key)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success()


class Collect(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_connected = True
        self.binance_id = None

    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = user_info["kakao_id"]
            binance_api_key = UserServices.get_binance_api_key(kakao_id)

            self.collect(binance_api_key)
            self.save(kakao_id)
            # DB에서 데이터 불러오기
            # self.load_data()
            # 3개 DB에 저장되어 있는 데이터를 연산법 적용 후 return
            #self.process_position_data()

            profile = UserServices.get_profile(kakao_id)
            #transaction = 
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "profile": profile,
                #transaction 여기에다가 넣어주기기
            },
        )

    def collect(self, binance_api_key):
        self.is_connected = BinanceApiServices.is_connected(binance_api_key)

        if self.is_connected:
            self.binance_id = BinanceApiServices.get_binance_id(binance_api_key)
            self.all_orders_data = BinanceApiServices.get_orders_data(binance_api_key)
            self.trades_data = BinanceApiServices.get_trades_data(binance_api_key)
            self.transactions_data = BinanceApiServices.get_transactions_data(binance_api_key)
            

    def save(self, kakao_id):
        UserServices.save_is_connected(kakao_id, self.is_connected)
        UserServices.save_binance_id(kakao_id, self.binance_id)
        # UserServices.save_all_order(self.binance_id, self.all_orders_data)
        # UserServices.save_trades_data(self.binance_id, self.trades_data)
        # UserServices.save_transactions_data(self.binance_id, self.transactions_data)
    # 25.02.19 윤택한
    # DB에서 데이터 불러오기
    # def load_data(self):
        # self.all_orders_data = UserServices.get_all_orders(self.binance_id)
        # self.trades_data = UserServices.get_trades_data(self.binance_id)
        # self.transactions_data = UserServices.get_transactions_data(self.binance_id)
    # 25.02.19 윤택한
    # Orders, Trades, Transactions 데이터를 하나로 합쳐 처리 후 저장하는 과정이 들어간 함수
    #def process_position_data():


class Profile(APIView):
    def get(self, request) -> JsonResponse:
        try:
            user_info = request.session.get("user_info")
            kakao_id = user_info["kakao_id"]
            profile = UserServices.get_profile(kakao_id)
        except Exception as e:
            print(e)
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "profile": profile,
            },
        )