from collections import defaultdict
from datetime import datetime
from decimal import Decimal

from applications.users.services import UserKeyInfoServices
from applications.binance_api.services import BinanceApiServices
from applications.transaction.repositories import (
    PositionHistoryRepository,
    OrdersRepository,
)
from applications.transaction.dtos import PositionDto


class PositionCalculatorServices:
    @staticmethod
    def calculate_position(kakao_id, binance_api_key):
        binance_id = UserKeyInfoServices.get_binance_id(kakao_id)
        quantity_dict = PositionCalculatorServices.get_quantity_dict(binance_api_key)
        last_closed_at = PositionHistoryRepository.get_last_closed_at(binance_id)
        orders = OrdersRepository.get_order_summary(binance_id, last_closed_at)

        in_progress_position_dto_dict = {}
        completed_position_dto_list = []

        for order in orders:
            symbol = order["symbol"]
            executed_quantity = order["executed_quantity"]

            if symbol not in in_progress_position_dto_dict:
                position_dto = PositionDto(
                    binance_id=binance_id,
                    symbol=symbol,
                    position="SHORT" if order["side"] == "BUY" else "LONG",
                    position_closed_at=order["time"],
                )
                in_progress_position_dto_dict[symbol] = position_dto

            quantity_dict[symbol] += executed_quantity
            in_progress_position_dto_dict[symbol].insert_order(order)

            if quantity_dict[symbol] == 0:
                position_dto = in_progress_position_dto_dict[symbol]
                position_dto.calculate()
                completed_position_dto_list.append(position_dto)
                del in_progress_position_dto_dict[symbol]

        return completed_position_dto_list

    @staticmethod
    def get_quantity_dict(binance_api_key):
        data = BinanceApiServices.get_position_info_data(binance_api_key)
        quantity_dict = defaultdict(lambda: Decimal("0"))

        for position in data:
            symbol = position["symbol"]
            quantity_dict[symbol] = Decimal(position["position_amt"])

        return quantity_dict
