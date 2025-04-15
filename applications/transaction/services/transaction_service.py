from datetime import datetime, timedelta

from django.db import transaction

from applications.transaction.models import PositionHistory, PositionOrders
from applications.transaction.repositories import PositionHistoryRepository


class TransactionService:
    @staticmethod
    def save_position(position_dto_lsit):
        with transaction.atomic():
            for position_dto in position_dto_lsit:
                position_history_obj = PositionHistory.objects.create(
                    **position_dto.to_position_history_data()
                )

                position_order_data = position_dto.to_position_order_data(
                    position_history_obj.id
                )
                PositionOrders.objects.bulk_create(
                    [PositionOrders(**order_data) for order_data in position_order_data]
                )

    @staticmethod
    def get_position_by_date(binance_id, start_date=None, end_date=None):
        now = datetime.now()
        if start_date is None:
            start_date = int((now - timedelta(days=7)).timestamp())
        if end_date is None:
            end_date = int(now.timestamp())

        transaction = PositionHistoryRepository.get_position_by_date(
            binance_id, start_date, end_date
        )

        return TransactionService.format_transaction(transaction)

    @staticmethod
    def format_transaction(transaction):
        formatted = []
        for item in transaction:
            realized_pnl = float(item.realized_pnl)

            data = {
                "positionClosed": datetime.fromtimestamp(
                    item.position_closed_at / 1000
                ).strftime("%Y-%m-%d %H:%M:%S"),
                "positionDuration": TransactionService.format_duration(
                    item.position_duration // 1000
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

        parts = []

        if hours > 0:
            parts.append(f"{hours}시간")
        if minutes > 0 or not parts:
            parts.append(f"{minutes}분")

        return " ".join(parts)

    @staticmethod
    def format_number(value) -> str:
        try:
            return f"{float(value):,.2f}"
        except (TypeError, ValueError):
            return "0.00"
