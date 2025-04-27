from django.db import models
from django.utils import timezone


class PositionOrders(models.Model):
    id = models.AutoField(primary_key=True)
    binance_uid = models.BigIntegerField(db_column="binanceUid")
    position_history_id = models.BigIntegerField(db_column="positionHistoryId")
    order_history_id = models.BigIntegerField(db_column="orderHistoryId")
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "PositionOrders"
        managed = False
