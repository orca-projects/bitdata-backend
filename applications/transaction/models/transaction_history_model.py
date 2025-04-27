from django.db import models
from django.utils import timezone


class TransactionHistory(models.Model):
    id = models.AutoField(primary_key=True)
    binance_uid = models.BigIntegerField(db_column="binanceUid")
    symbol = models.CharField(max_length=20, null=True, blank=True)
    tran_id = models.BigIntegerField(db_column="tranId")
    trade_id = models.BigIntegerField(db_column="tradeId", null=True, blank=True)
    time = models.DateTimeField()
    info = models.CharField(max_length=255, null=True, blank=True)
    income_type = models.CharField(db_column="incomeType", max_length=30)
    income = models.DecimalField(max_digits=20, decimal_places=6)
    asset = models.CharField(max_length=10)
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "TransactionHistory"
        unique_together = ("binance_uid", "symbol", "tran_id", "income_type")
        managed = False
