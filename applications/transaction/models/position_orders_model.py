from django.db import models
from django.utils import timezone

from applications.users.models import UserBinance
from applications.transaction.models import PositionHistory, OrderHistory


class PositionOrders(models.Model):
    binance_uid = models.ForeignKey(
        UserBinance,
        to_field="binance_uid",
        on_delete=models.CASCADE,
        db_column="binanceUid",
    )
    position_history = models.ForeignKey(
        PositionHistory, on_delete=models.CASCADE, db_column="positionHistoryId"
    )
    order_history = models.ForeignKey(
        OrderHistory, on_delete=models.CASCADE, db_column="orderHistoryId"
    )
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "PositionOrders"
        managed = False
