from django.utils import timezone
from django.db import transaction
from core.utils import DateUtil
from applications.transaction.repositories import (
    PositionHistoryRepository,
    PositionOrdersRepository,
)


class TransactionService:
    @staticmethod
    def save_position(position_dto_list):
        with transaction.atomic():
            position_data_list = [
                dto.to_position_history_data() for dto in position_dto_list
            ]
            position_histories = PositionHistoryRepository.create(position_data_list)
            history_map = {ph.hash: ph.id for ph in position_histories}

            position_orders_data = []
            for dto in position_dto_list:
                position_history_id = history_map.get(dto.hash)
                if not position_history_id:
                    continue

                orders = dto.to_position_orders_data()
                for order in orders:
                    order["position_history_id"] = position_history_id
                    order["position_hash"] = dto.hash
                    position_orders_data.append(order)

            PositionOrdersRepository.create(position_orders_data)

    @staticmethod
    def get_position_by_date(binance_uid, start_ms=None, end_ms=None):
        now = timezone.now()

        if start_ms is None:
            start_ms = now - timezone.timedelta(days=7)
        else:
            start_ms = DateUtil.parse_timestamp_to_datetime(start_ms)

        if end_ms is None:
            end_ms = now
        else:
            end_ms = DateUtil.parse_timestamp_to_datetime(end_ms)

        transaction = PositionHistoryRepository.get_position_by_date(
            binance_uid, start_ms, end_ms
        )

        return TransactionService.format_transaction(transaction)

    @staticmethod
    def format_transaction(transaction):
        formatted = []
        for item in transaction:
            realized_pnl = float(item.realized_pnl)

            data = {
                "positionClosed": timezone.localtime(item.position_closed_at).strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),
                "positionDuration": TransactionService.format_duration(
                    item.position_duration
                ),
                "position": item.position,
                "symbol": item.symbol,
                "totalBuy": TransactionService.format_number(item.opening_size),
                "totalSell": TransactionService.format_number(item.closing_size),
                "pnl": TransactionService.format_number(item.trade_pnl),
                "finalPnl": TransactionService.format_number(realized_pnl),
                "totalBuyFee": TransactionService.format_number(
                    item.opening_commission
                ),
                "totalSellFee": TransactionService.format_number(
                    item.closing_commission
                ),
                "totalFundingCost": TransactionService.format_number(
                    item.total_funding_fee
                ),
                "totalFee": TransactionService.format_number(item.total_commission),
                "finalRoi": TransactionService.format_number(item.realized_roi),
                "avgBuy": TransactionService.format_number(item.opening_avg_price),
                "avgSell": TransactionService.format_number(item.closing_avg_price),
                "winlose": (
                    "win"
                    if realized_pnl > 0
                    else "lose" if realized_pnl < 0 else "even"
                ),
            }
            formatted.append(data)
        return formatted

    @staticmethod
    def format_duration(seconds: int) -> str:
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60

        parts = []

        if hours > 0:
            parts.append(f"{hours}시간")
        if minutes > 0:
            parts.append(f"{minutes}분")
        if secs > 0 or not parts:
            parts.append(f"{secs}초")

        return " ".join(parts)

    @staticmethod
    def format_number(value) -> str:
        try:
            return f"{float(value):,.2f}"
        except (TypeError, ValueError):
            return "0.00"
