from dataclasses import dataclass, field
from decimal import ROUND_HALF_UP, Decimal
from datetime import datetime, timedelta
from django.utils import timezone

from applications.transaction.repositories import TransactionsRepository


@dataclass
class PositionDto:
    binance_id: str
    position_closed_at: int
    position: str
    symbol: str

    position_duration: int = field(default=0)
    opening_size: Decimal = Decimal("0")
    closing_size: Decimal = Decimal("0")
    trade_pnl: Decimal = Decimal("0")
    realized_pnl: Decimal = Decimal("0")
    realized_roi: Decimal = Decimal("0")
    opening_avg_price: Decimal = Decimal("0")
    closing_avg_price: Decimal = Decimal("0")
    opening_commission: Decimal = Decimal("0")
    closing_commission: Decimal = Decimal("0")
    total_funding_fee: Decimal = Decimal("0")
    total_commission: Decimal = Decimal("0")

    _order_ids: list[str] = field(default_factory=list)
    _position_opened_at: datetime = field(default_factory=timezone.now)
    _open_quantity: int = field(default=0)
    _close_quantity: int = field(default=0)

    def insert_order(self, order: dict):
        self._order_ids.append(order["order_id"])

        side = order["side"]
        executed_quantity = order["executed_quantity"]
        size = order["size"]
        commission = order["commission"]

        if self.position == "LONG":
            if side == "BUY":
                self._open_quantity += executed_quantity
                self.opening_size += size
                self.opening_avg_price += size
                self.opening_commission += commission

            if side == "SELL":
                self._close_quantity += executed_quantity
                self.closing_size += size
                self.closing_avg_price += size
                self.closing_commission += commission

        else:
            if side == "SELL":
                self._open_quantity += executed_quantity
                self.opening_size += size
                self.opening_avg_price += size
                self.opening_commission += commission

            if side == "BUY":
                self._close_quantity += executed_quantity
                self.closing_size += size
                self.closing_avg_price += size
                self.closing_commission += commission

        realized_pnl = order["realized_pnl"]
        self.trade_pnl += realized_pnl

        time = order["time"]
        self._position_opened_at = time

    def calculate(self):
        self.calculate_total_funding_fee()
        self.calculate_total_commission()

        self.calculate_position_duration()
        self.calculate_realized_pnl()
        self.calculate_realized_roi()
        self.calculate_avg_price()

    def calculate_position_duration(self):
        self.position_duration = self.position_closed_at - self._position_opened_at

    def calculate_realized_pnl(self):
        self.realized_pnl = self.trade_pnl + self.total_commission

    def calculate_realized_roi(self):
        if self.closing_size > 0:
            roi = self.realized_pnl / self.closing_size * 100
            self.realized_roi = roi.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        else:
            self.realized_roi = Decimal("0.00")

    def calculate_avg_price(self):
        self.opening_avg_price = abs(self.opening_avg_price / self._open_quantity)
        self.closing_avg_price = abs(self.closing_avg_price / self._close_quantity)

    def calculate_total_funding_fee(self):
        self.total_funding_fee = TransactionsRepository.get_total_funding_fee(
            self.symbol, self._position_opened_at, self.position_closed_at
        )

    def calculate_total_commission(self):
        self.total_commission = (
            self.opening_commission + self.closing_commission + self.total_funding_fee
        )

    def to_position_history_data(self):
        return {
            "binance_id": self.binance_id,
            "position_closed_at": self.position_closed_at,
            "position": self.position,
            "position_duration": self.position_duration,
            "symbol": self.symbol,
            "opening_size": self.opening_size,
            "closing_size": self.closing_size,
            "trade_pnl": self.trade_pnl,
            "realized_pnl": self.realized_pnl,
            "realized_roi": self.realized_roi,
            "opening_avg_price": self.opening_avg_price,
            "closing_avg_price": self.closing_avg_price,
            "opening_commission": self.opening_commission,
            "closing_commission": self.closing_commission,
            "total_funding_fee": self.total_funding_fee,
            "total_commission": self.total_commission,
        }

    def to_position_order_data(self, position_id: int):
        return [
            {
                "binance_id": self.binance_id,
                "order_id": order_id,
                "position_id": position_id,
            }
            for order_id in self._order_ids
        ]
