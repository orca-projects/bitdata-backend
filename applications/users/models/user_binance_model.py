from django.db import models
from django.utils import timezone


class UserBinance(models.Model):
    binance_uid = models.BigIntegerField(db_column="binanceUid", unique=True)
    last_collected = models.DateTimeField(
        db_column="lastCollected", null=True, blank=True
    )
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "UserBinance"
        managed = False
