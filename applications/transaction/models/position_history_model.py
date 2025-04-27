from django.db import models
from django.utils import timezone


class PositionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    binance_uid = models.BigIntegerField(db_column="binanceUid")
    position_closed_at = models.DateTimeField(db_column="positionClosedAt")
    position = models.CharField(max_length=5)
    position_duration = models.BigIntegerField(db_column="positionDuration")
    symbol = models.CharField(max_length=20)
    opening_size = models.DecimalField(
        db_column="openingSize", max_digits=20, decimal_places=6
    )
    closing_size = models.DecimalField(
        db_column="closingSize", max_digits=20, decimal_places=6
    )
    trade_pnl = models.DecimalField(
        db_column="tradePnl", max_digits=20, decimal_places=6
    )
    realized_pnl = models.DecimalField(
        db_column="realizedPnl", max_digits=20, decimal_places=6
    )
    realized_roi = models.DecimalField(
        db_column="realizedRoi", max_digits=20, decimal_places=6
    )
    opening_avg_price = models.DecimalField(
        db_column="openingAvgPrice", max_digits=20, decimal_places=6
    )
    closing_avg_price = models.DecimalField(
        db_column="closingAvgPrice", max_digits=20, decimal_places=6
    )
    opening_commission = models.DecimalField(
        db_column="openingCommission", max_digits=20, decimal_places=6
    )
    closing_commission = models.DecimalField(
        db_column="closingCommission", max_digits=20, decimal_places=6
    )
    total_funding_fee = models.DecimalField(
        db_column="totalFundingFee", max_digits=20, decimal_places=6
    )
    total_commission = models.DecimalField(
        db_column="totalCommission", max_digits=20, decimal_places=6
    )
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "PositionHistory"
        managed = False
