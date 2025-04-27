from django.db import models
from django.utils import timezone


class UserApiKey(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(db_column="userId")
    binance_api_key = models.CharField(db_column="binanceApiKey", max_length=64)
    binance_secret_key = models.CharField(db_column="binanceSecretKey", max_length=64)
    user_binance_id = models.BigIntegerField(db_column="userBinanceId")
    is_key_active = models.BooleanField(db_column="isKeyActive", default=True)
    is_connected = models.BooleanField(db_column="isConnected", default=False)
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "UserApiKey"
        managed = False
