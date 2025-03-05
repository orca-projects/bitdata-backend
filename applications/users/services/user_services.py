from applications.users.repositories import UserRepository, UserKeyInfoRepository, OrdersRepository, TradesRepository, TransactionsRepository, PositionOrdersRepository
import re
import pandas as pd
from datetime import datetime, timedelta
from django.utils.timezone import make_aware
from collections import defaultdict
from django.db.models import F
from datetime import datetime, timedelta

class UserServices:
    @staticmethod
    def is_member(kakao_id):
        user_kakao = UserRepository.find_by_kakao_id(kakao_id)
        return user_kakao is not None

    @staticmethod
    def has_binance_api_key(kakao_id):
        user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        return user_key_info is not None

    @staticmethod
    def save_binance_api_key(kakao_id, binance_api_key):
        UserServices.deactivate_active_user_key_info(kakao_id)

        UserKeyInfoRepository.create_user_key_info(kakao_id, binance_api_key)

    @staticmethod
    def deactivate_active_user_key_info(kakao_id):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        if active_user_key_info:
            UserKeyInfoRepository.update_user_key_info(
                active_user_key_info, is_key_active=False
            )

    @staticmethod
    def get_binance_api_key(kakao_id):
        user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)

        binance_api_key = {
            "api_key": user_key_info.binance_api_key,
            "secret_key": user_key_info.binance_secret_key,
        }
        return binance_api_key
    
    # 25.02.27(목) 윤택한
    # last collected 깂에 대하여 유효성 검사
    @staticmethod
    def get_last_collected(binance_id):
        last_collected = UserKeyInfoRepository.get_last_collected(binance_id)
        
        # last_collected이 None이면 바로 반환
        if last_collected is None:
            return None

        # last_collected이 datetime인지 확인 후 반환
        return last_collected if isinstance(last_collected, datetime) else None

    
    @staticmethod
    def save_is_connected(kakao_id, is_connected):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        UserKeyInfoRepository.update_user_key_info(
            active_user_key_info, is_connected=is_connected
        )

    @staticmethod
    def save_binance_id(kakao_id, binance_id):
        active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(kakao_id)
        UserKeyInfoRepository.update_user_key_info(
            active_user_key_info, binance_id=binance_id
        )

    @staticmethod
    def save_last_collected(binance_id, last_collected):
        active_user_key_info = UserKeyInfoRepository.find_active_by_binance_id(binance_id)
        UserKeyInfoRepository.update_user_key_info(
            active_user_key_info, last_collected=last_collected
        )

    @staticmethod
    def get_next_position_id(binance_id):
        last_position = PositionOrdersRepository.get_max_position_id(binance_id)
        return UserServices.generate_next_position_id(last_position, binance_id)

    # 25.02.26(수) 윤택한 생성
    # 해당 바이낸스 ID의 PositionId의 최대값을 가져와서 +1한 값을 return(없을 시 초기 값 return)
    @staticmethod
    def generate_next_position_id(last_position, binance_id):
        if last_position:
            return last_position + 1  # 기존 문자열 처리 제거 후 정수 연산

        return 1  # 초기값 (DB가 bigint이므로 최소값을 1로 설정)
    # 25.02.16(일) 윤택한 생성
    #
    @staticmethod
    def save_all_order(binance_id, orders_data):
        OrdersRepository.save_orders_data(
            binance_id, orders_data=orders_data
        )
    
    @staticmethod
    def save_trades_data(binance_id, trades_data):
        TradesRepository.save_trades_data(
            binance_id, trades_data=trades_data
        )
    
    @staticmethod
    def save_transactions_data(binance_id, transactions_data):
        TransactionsRepository.save_transactions_data(
            binance_id, transactions_data=transactions_data
        )

    @staticmethod
    def save_positions_data(positions_data):
        PositionOrdersRepository.save_positions_data(
            positions_data
        )


    @staticmethod
    def get_profile(kakao_id):
        try:
            user_kakao = UserRepository.find_by_kakao_id(kakao_id)
            username = user_kakao.name

            active_user_key_info = UserKeyInfoRepository.find_active_by_kakao_id(
                kakao_id
            )
            is_connected = active_user_key_info.is_connected
            api_key = active_user_key_info.binance_api_key
            binance_uid = active_user_key_info.binance_id

            username_masked = UserServices.mask_username(username)
            api_key_masked = UserServices.mask_api_key(api_key)

            return {
                "username": username_masked,
                "is_connected": is_connected,
                "api_key": api_key_masked,
                "binance_uid": binance_uid,
            }
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return None

    @staticmethod
    def mask_username(username):
        if len(username) == 1:
            return "*"
        elif len(username) == 2:
            return f"{username[0]}*"
        elif len(username) == 3:
            return f"{username[0]}*{username[2]}"
        else:
            return f"{username[0]}{'*' * (len(username) - 2)}{username[-1]}"

    @staticmethod
    def mask_api_key(api_key):
        return api_key[0] + "****" + api_key[-1]
    
    # 25.02.27 윤택한
    # orders_data orderId별로 그룹화 하는 기능
    @staticmethod
    def process_positions(binance_id, start_position_id, all_orders_data):

        # 데이터 정리
        df_orders = pd.DataFrame(all_orders_data)
        df_orders = df_orders[df_orders["positionSide"] == "BOTH"].copy()
        df_orders = df_orders.sort_values(by=["symbol", "time"]).reset_index(drop=True)
        df_orders["executedQty"] = df_orders["executedQty"].astype(float)

        if df_orders.empty:
            return None

        # position_id 초기화
        position_counter = int(start_position_id.split("_")[-1])
        positions = []
        current_position = {
            "buys": 0.0,
            "sells": 0.0,
            "order_ids": [],
            "position_id": start_position_id,
            "side": None  # 포지션 방향 (BUY or SELL)
        }

        # 포지션 그룹핑 (모든 주문 포함)
        for _, row in df_orders.iterrows():
            symbol = row["symbol"]  # SYMBOL 값 가져오기
            formatted_order_id = f"{symbol}_{row['orderId']}"  # `{SYMBOL}_orderId` 형식으로 변환

            current_position["order_ids"].append(formatted_order_id)

            # 첫 번째 주문의 방향 설정
            if current_position["side"] is None:
                current_position["side"] = row["side"]

            if row["side"] == "BUY":
                current_position["buys"] += row["executedQty"]
            elif row["side"] == "SELL":
                current_position["sells"] += row["executedQty"]

            # 포지션 종료 조건 확인 (BUY == SELL 또는 SELL == BUY)
            if abs(current_position["buys"] - current_position["sells"]) < 1e-6:
                for order_id in current_position["order_ids"]:
                    positions.append({
                        "binanceId": binance_id,
                        "orderId": order_id,  # `{SYMBOL}_orderId` 형식으로 변경됨
                        "positionId": current_position["position_id"]
                    })
                position_counter += 1
                current_position = {
                    "buys": 0.0,
                    "sells": 0.0,
                    "order_ids": [],
                    "position_id": f"{binance_id}_{str(position_counter).zfill(6)}",
                    "side": None
                }

        return positions  # JSON 형태 반환
    

    # 25.02.28(금)
    # 트랜잭션 데이터 가공
    @staticmethod
    def process_transactions(binance_id):
        if not binance_id:
            return {}

        binance_id = str(binance_id)
        transactions_data = {
            "positions": []
        }

        # 1. 해당 binance_id의 모든 PositionOrders 데이터 가져오기
        positions = PositionOrdersRepository.get_positions(binance_id)
        if not positions:
            return {}  # 포지션 데이터가 없으면 빈 딕셔너리 반환

        # 2. position_id별로 PositionOrders를 그룹화
        position_groups = defaultdict(list)
        for position in positions:
            position_groups[position.position_id].append(position)

        # 3. 각 포지션에 대해 유지 기간, 종료 시간, 포지션 방향 및 심볼 설정
        position_durations = []
        for position_id, pos_orders in position_groups.items():
            if not pos_orders:
                continue

            # order_id에서 symbol 추출 (첫 번째 orderId의 앞부분 가져오기)
            first_order_id = pos_orders[0].order_id
            symbol = first_order_id.split('_')[0]  # "SYMBOL" 추출

            # order_id에서 symbol 제거하여 순수한 orderId 추출
            order_numbers = [
                int(pos.order_id.split('_')[1]) for pos in pos_orders
            ]

            # 최소 및 최대 orderId 찾기
            min_order_number = min(order_numbers)
            max_order_number = max(order_numbers)

            # 해당 orderId  Orders 데이터 조회
            min_order = OrdersRepository.get_order_by_order_id(str(min_order_number))
            max_order = OrdersRepository.get_order_by_order_id(str(max_order_number))

            if min_order and max_order:
                # update_time을 datetime 객체로 변환
                min_update_time = datetime.fromtimestamp(min_order.update_time / 1000)
                max_update_time = datetime.fromtimestamp(max_order.update_time / 1000)

                # 포지션 유지 기간 계산
                duration = max_update_time - min_update_time
                duration_str = str(duration)  # HH:MM:SS 형식으로 변환

                # 포지션 종료 시간 (YYYYMMDD HHMMSS 형식)
                position_closed_str = max_update_time.strftime("%Y%m%d %H%M%S")

                # 포지션 방향 (LONG or SHORT) 결정
                order_ids = [pos.order_id.split('_')[1] for pos in pos_orders]
                orders = OrdersRepository.get_orders_by_order_ids(order_ids)

                if orders:
                    first_order = orders.first()
                    last_order = orders.last()

                    if first_order and last_order:
                        if first_order.side == "BUY" and last_order.side == "SELL":
                            position_type = "LONG"
                            target_buy_side = "BUY" 
                            target_sell_side = "SELL"
                        elif first_order.side == "SELL" and last_order.side == "BUY":
                            position_type = "SHORT"
                            target_buy_side = "BUY" 
                            target_sell_side = "SELL" 
                        else:
                            position_type = "UNKNOWN"
                            target_buy_side = None
                            target_sell_side = None

                        # total_buy 계산 (포지션을 늘리는 주문) → executedQty * avgPrice 적용
                        total_buy = sum(float(order.executed_qty) * float(order.avg_price) for order in orders if order.side == target_buy_side) if target_buy_side else 0.0

                        # total_sell 계산 (포지션을 줄이는 주문) → executedQty * avgPrice 적용
                        total_sell = sum(float(order.executed_qty) * float(order.avg_price) for order in orders if order.side == target_sell_side) if target_sell_side else 0.0

                        # PNL (손익) 계산 → total_sell - total_buy
                        pnl = total_sell - total_buy

                        # total_buy_fee 계산 (BUY 주문들의 commission 합산)
                        buy_order_ids = [order.order_id for order in orders if order.side == target_buy_side]
                        trades = TradesRepository.get_trades_by_binance_id_and_order_ids(binance_id, buy_order_ids)

                        total_buy_fee = sum(float(trade.commission) for trade in trades) if trades else 0.0

                        # 결과 저장
                        position_durations.append({
                            "position_id": position_id,
                            "position_duration": duration_str,
                            "position_closed": position_closed_str,
                            "position": position_type,  
                            "symbol": symbol,  
                            "total_buy": f"{total_buy:,.2f}",  
                            "total_sell": f"{total_sell:,.2f}", 
                            "pnl": f"{pnl:,.2f}", 
                            #"total_buy_fee": f"{total_buy_fee:,.8f}"  # 총 매수 수수료 추가
                        })

        # 최종 데이터 저장
        transactions_data["positions"] = position_durations

        return transactions_data