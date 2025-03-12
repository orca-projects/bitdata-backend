from django.http import JsonResponse

from rest_framework.views import APIView

from django.utils.timezone import now

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
        self.last_position_id = None
        self.all_orders_data = None
        self.trades_data = None
        self.transactions_data = None
        self.profile = None

    def get(self, request) -> JsonResponse:
        try:
            kakao_id, binance_api_key = self.fetch_user_data(
                request
            )  # 사용자 정보 가져오기

            self.binance_id = BinanceApiServices.get_binance_id(
                binance_api_key
            )  # 바이낸스ID 가져오기

            last_collected = self.get_last_collected(
                self.binance_id
            )  # 추후에 이 값을 통해서 BinanceId 조회해야 함

            self.collect(binance_api_key)  # 바이낸스 데이터 가져오기

            self.save(kakao_id)  # 상태 저장

            self.last_position_id = self.get_next_position_id(
                self.binance_id
            )  # 마지막 포지션 ID 조회

            if self.all_orders_data:  # 주문 데이터가 있을 경우 포지션 처리
                positions_data = self.process_positions(
                    self.binance_id, self.last_position_id
                )

                if positions_data:  # 데이터가 존재할 때만 저장
                    self.save_positions_data(positions_data)

            transactions = self.process_transactions(self.binance_id)
            print("Transactions 데이터", transactions)

            self.profile = UserServices.get_profile(kakao_id)  # 프로필 데이터 조회
        except Exception as e:
            print(f"Error in Collect.get(): {e}")
            return ResponseHelper.error()

        return ResponseHelper.success(
            data={
                "profile": self.profile,
                # transactions 여기에다가 넣어주기기
            },
        )

    def fetch_user_data(self, request):
        user_info = request.session.get("user_info", {})
        kakao_id = user_info.get("kakao_id")
        binance_api_key = UserServices.get_binance_api_key(kakao_id)
        return kakao_id, binance_api_key

    @staticmethod
    def get_last_collected(binance_id):
        if not binance_id:
            return None
        return UserServices.get_last_collected(binance_id)

    def collect(self, binance_api_key):
        self.is_connected = BinanceApiServices.is_connected(binance_api_key)
        if not self.is_connected:
            return  # 연결되지 않으면 종료

        # 데이터 수집과 동시에 lastCollected 업데이트
        last_collected_time = now()
        UserServices.save_last_collected(self.binance_id, last_collected_time)

        self.position_info = BinanceApiServices.get_position_info_data(binance_api_key)
        self.all_orders_data = BinanceApiServices.get_orders_data(binance_api_key)
        self.trades_data = BinanceApiServices.get_trades_data(binance_api_key)
        self.transactions_data = BinanceApiServices.get_transactions_data(
            binance_api_key
        )

    def get_next_position_id(self, binance_id):
        if not binance_id:
            print(f"Binance Id가 없습니다")
            return 1
        return UserServices.get_next_position_id(binance_id)

    def save(self, kakao_id):
        UserServices.save_is_connected(kakao_id, self.is_connected)
        UserServices.save_binance_id(kakao_id, self.binance_id)
        UserServices.save_all_order(self.binance_id, self.all_orders_data)
        UserServices.save_trades_data(self.binance_id, self.trades_data)
        UserServices.save_transactions_data(self.binance_id, self.transactions_data)

    # 25.02.27(목) 윤택한
    # Order 데이터 가지고 그룹화
    def process_positions(self, binance_id, start_position_id):
        if not self.all_orders_data:
            return []

        return UserServices.process_positions(
            binance_id, start_position_id, self.all_orders_data
        )

    # 25.02.27(목) 윤택한
    # position_data 저장
    @staticmethod
    def save_positions_data(positions_data):
        UserServices.save_positions_data(positions_data)

    # 25.03.05(수) 윤택한
    # transaction 데이터 가공 후 가져오기
    @staticmethod
    def process_transactions(binance_id):
        return UserServices.process_transactions(binance_id)


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
