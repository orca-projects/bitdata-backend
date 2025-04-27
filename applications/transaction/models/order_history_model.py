from django.db import models
from django.utils import timezone

from applications.users.models import UserBinance


class OrderHistory(models.Model):
    id = models.AutoField(primary_key=True)
    binance_uid = models.BigIntegerField(db_column="binanceUid")
    symbol = models.CharField(max_length=20)
    order_id = models.BigIntegerField(db_column="orderId")
    client_order_id = models.CharField(db_column="clientOrderId", max_length=36)
    time = models.DateTimeField()
    update_time = models.DateTimeField(db_column="updateTime")
    side = models.CharField(max_length=4)
    position_side = models.CharField(db_column="positionSide", max_length=5)
    status = models.CharField(max_length=20)
    type = models.CharField(max_length=25)
    orig_type = models.CharField(db_column="origType", max_length=25)
    time_in_force = models.CharField(db_column="timeInForce", max_length=3)
    avg_price = models.DecimalField(
        db_column="avgPrice", max_digits=20, decimal_places=6
    )
    executed_qty = models.DecimalField(
        db_column="executedQty", max_digits=20, decimal_places=6
    )
    orig_qty = models.DecimalField(db_column="origQty", max_digits=20, decimal_places=6)
    price = models.DecimalField(max_digits=20, decimal_places=6)
    stop_price = models.DecimalField(
        db_column="stopPrice", max_digits=20, decimal_places=6
    )
    reduce_only = models.BooleanField(db_column="reduceOnly", default=False)
    close_position = models.BooleanField(db_column="closePosition", default=False)
    working_type = models.CharField(db_column="workingType", max_length=20)
    price_protect = models.BooleanField(db_column="priceProtect", default=False)
    price_match = models.CharField(
        db_column="priceMatch", max_length=10, default="NONE"
    )
    self_trade_prevention_mode = models.CharField(
        db_column="selfTradePreventionMode", max_length=20, default="NONE"
    )
    cum_quote = models.DecimalField(
        db_column="cumQuote", max_digits=20, decimal_places=6, default=0
    )
    good_till_date = models.BigIntegerField(db_column="goodTillDate", default=0)
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "OrderHistory"
        unique_together = ("binance_uid", "symbol", "order_id")
        managed = False
