from django.db import models


class PositionOrders(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.CharField(max_length=50, db_column="binanceId")
    order_id = models.CharField(max_length=50, db_column="orderId")
    position = models.ForeignKey(
        "PositionHistory",
        on_delete=models.CASCADE,
        db_column="positionId",
        related_name="position_orders",
    )
    created_at = models.DateTimeField(auto_now_add=True, db_column="createdAt")

    class Meta:
        db_table = "PositionsOrders"
        verbose_name = "Position Order"
        verbose_name_plural = "Position Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"[{self.binance_id}] Position: {self.position_id}, Order: {self.order_id}"
        )
