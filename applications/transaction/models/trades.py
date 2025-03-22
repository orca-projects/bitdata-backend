from django.db import models
from django.utils import timezone


class Trades(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.CharField(max_length=255, db_column="binanceId")
    buyer = models.BooleanField(db_column="buyer")
    commission = models.CharField(max_length=255, db_column="commission")
    commission_asset = models.CharField(max_length=255, db_column="commissionAsset")
    trade_id = models.CharField(max_length=255, db_column="tradeId")
    maker = models.BooleanField(db_column="maker")
    order_id = models.CharField(max_length=255, db_column="orderId")
    price = models.CharField(max_length=255, db_column="price")
    qty = models.CharField(max_length=255, db_column="qty")
    quote_qty = models.CharField(max_length=255, db_column="quoteQty")
    realized_pnl = models.CharField(max_length=255, db_column="realizedPnl")
    side = models.CharField(max_length=255, db_column="side")
    position_side = models.CharField(max_length=255, db_column="positionSide")
    symbol = models.CharField(max_length=255, db_column="symbol")
    time = models.BigIntegerField(db_column="time")
    created_at = models.DateTimeField(default=timezone.now, db_column="createdAt")

    class Meta:
        db_table = "Trades"
        managed = False

    def __str__(self):
        return f"Trade ID: {self.trade_id}, Symbol: {self.symbol}"
