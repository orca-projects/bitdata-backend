from django.db import models


class PositionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.CharField(max_length=50, db_column="binanceId")
    position_closed_at = models.BigIntegerField(db_column="positionClosedAt")
    position = models.CharField(max_length=5)
    position_duration = models.BigIntegerField(db_column="positionDuration")
    symbol = models.CharField(max_length=255)
    opening_size = models.DecimalField(
        max_digits=20, decimal_places=6, db_column="openingSize"
    )
    closing_size = models.DecimalField(
        max_digits=20, decimal_places=6, db_column="closingSize"
    )
    trade_pnl = models.DecimalField(
        max_digits=20, decimal_places=6, db_column="tradePnl"
    )
    realized_pnl = models.DecimalField(
        max_digits=20, decimal_places=6, db_column="realizedPnl"
    )
    realized_roi = models.DecimalField(
        max_digits=20, decimal_places=6, db_column="realizedRoi"
    )
    opening_avg_price = models.DecimalField(
        max_digits=20, decimal_places=6, db_column="openingAvgPrice"
    )
    closing_avg_price = models.DecimalField(
        max_digits=20, decimal_places=6, db_column="closingAvgPrice"
    )
    opening_commission = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True,
        db_column="openingCommission",
    )
    closing_commission = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True,
        db_column="closingCommission",
    )
    total_funding_fee = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True,
        db_column="totalFundingFee",
    )
    total_commission = models.DecimalField(
        max_digits=20,
        decimal_places=6,
        null=True,
        blank=True,
        db_column="totalCommission",
    )

    class Meta:
        db_table = "PositionHistory"
        verbose_name = "Position History"
        verbose_name_plural = "Position Histories"
        ordering = ["-position_closed_at"]

    def __str__(self):
        return f"[{self.binance_id}] {self.symbol} {self.position} - Closed at {self.position_closed_at.strftime('%Y-%m-%d %H:%M:%S')}"
