from django.db import models
from django.utils import timezone


class TradeHistory(models.Model):
    id = models.AutoField(primary_key=True)
    binance_uid = models.BigIntegerField(db_column="binanceUid")
    symbol = models.CharField(max_length=20)
    trade_id = models.BigIntegerField(db_column="tradeId")
    order_id = models.BigIntegerField(db_column="orderId")
    time = models.DateTimeField()
    side = models.CharField(max_length=4)
    position_side = models.CharField(db_column="positionSide", max_length=5)
    price = models.DecimalField(max_digits=20, decimal_places=6)
    qty = models.DecimalField(max_digits=20, decimal_places=6)
    quote_qty = models.DecimalField(
        db_column="quoteQty", max_digits=20, decimal_places=6
    )
    realized_pnl = models.DecimalField(
        db_column="realizedPnl", max_digits=20, decimal_places=6
    )
    buyer = models.BooleanField()
    maker = models.BooleanField()
    commission = models.DecimalField(max_digits=20, decimal_places=6)
    commission_asset = models.CharField(db_column="commissionAsset", max_length=10)
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "TradeHistory"
        unique_together = ("binance_uid", "symbol", "trade_id")
        managed = False
