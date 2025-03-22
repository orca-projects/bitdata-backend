from django.db import models
from django.utils import timezone


class Orders(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.CharField(max_length=255, db_column="binanceId")
    avg_price = models.CharField(max_length=255, db_column="avgPrice")
    client_order_id = models.CharField(max_length=255, db_column="clientOrderId")
    cum_quote = models.CharField(max_length=255, default="0", db_column="cumQuote")
    executed_qty = models.CharField(max_length=255, db_column="executedQty")
    order_id = models.CharField(max_length=255, db_column="orderId")
    orig_qty = models.CharField(max_length=255, db_column="origQty")
    orig_type = models.CharField(max_length=255, db_column="origType")
    price = models.CharField(max_length=255, db_column="price")
    reduce_only = models.BooleanField(default=False, db_column="reduceOnly")
    side = models.CharField(max_length=255, db_column="side")
    position_side = models.CharField(max_length=255, db_column="positionSide")
    status = models.CharField(max_length=255, db_column="status")
    stop_price = models.CharField(
        max_length=255, null=True, blank=True, db_column="stopPrice"
    )
    close_position = models.BooleanField(default=False, db_column="closePosition")
    symbol = models.CharField(max_length=255, db_column="symbol")
    time = models.BigIntegerField(db_column="time")
    time_in_force = models.CharField(max_length=255, db_column="timeInForce")
    type = models.CharField(max_length=255, db_column="type")
    update_time = models.BigIntegerField(db_column="updateTime")
    working_type = models.CharField(max_length=255, db_column="workingType")
    price_protect = models.BooleanField(default=False, db_column="priceProtect")
    price_match = models.CharField(
        max_length=255, default="NONE", db_column="priceMatch"
    )
    self_trade_prevention_mode = models.CharField(
        max_length=255, default="NONE", db_column="selfTradePreventionMode"
    )
    good_till_date = models.BigIntegerField(default=0, db_column="goodTillDate")
    created_at = models.DateTimeField(default=timezone.now, db_column="createdAt")

    class Meta:
        db_table = "Orders"
        managed = False

    def __str__(self):
        return f"Order ID: {self.order_id}, Symbol: {self.symbol}"
