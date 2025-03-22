from django.db import models
from django.utils import timezone


class Transactions(models.Model):
    id = models.AutoField(primary_key=True)
    binance_id = models.CharField(max_length=255, db_column="binanceId")
    symbol = models.CharField(max_length=255, db_column="symbol")
    income_type = models.CharField(max_length=255, db_column="incomeType")
    income = models.CharField(max_length=255, db_column="income")
    asset = models.CharField(max_length=255, db_column="asset")
    info = models.CharField(max_length=255, db_column="info")
    time = models.BigIntegerField(db_column="time")
    tran_id = models.CharField(max_length=255, db_column="tranId")
    trade_id = models.CharField(max_length=255, db_column="tradeId")
    created_at = models.DateTimeField(default=timezone.now, db_column="createdAt")

    class Meta:
        db_table = "Transactions"
        managed = False

    def __str__(self):
        return f"Transaction ID: {self.tran_id}, Asset: {self.asset}"
