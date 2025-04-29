from collections import defaultdict
from decimal import Decimal

from applications.users.services import UserApiKeyService
from applications.users.repositories import UserBinanceRepository
from applications.binance_api.services import BinanceApiServices
from applications.transaction.repositories import (
    PositionHistoryRepository,
    OrderHistoryRepository,
)
from applications.transaction.dtos import PositionDto


class PositionCalculatorService:
    @staticmethod
    def calculate_position(kakao_uid, binance_api_key):
        binance_uid = UserApiKeyService.get_binance_uid(kakao_uid)
        quantity_dict = PositionCalculatorService.get_quantity_dict(binance_api_key)
        last_closed_at = PositionHistoryRepository.get_last_closed_at(binance_uid)
        order_history_arr = OrderHistoryRepository.get_order_summary(
            binance_uid, last_closed_at
        )

        in_progress_position_dto_dict = {}
        completed_position_dto_list = []

        for order_history in order_history_arr:
            symbol = order_history["symbol"]
            executed_quantity = order_history["executed_quantity"]

            if symbol not in in_progress_position_dto_dict:
                position_dto = PositionDto(
                    binance_uid=binance_uid,
                    symbol=symbol,
                    position="SHORT" if order_history["side"] == "BUY" else "LONG",
                )
                in_progress_position_dto_dict[symbol] = position_dto

            quantity_dict[symbol] += executed_quantity
            in_progress_position_dto_dict[symbol].insert_order_history(order_history)

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
