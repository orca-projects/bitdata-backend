from django.db import models
from django.utils import timezone

from applications.users.models import User, UserBinance


class UserApiKey(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    binance_api_key = models.CharField(db_column="binanceApiKey", max_length=64)
    binance_secret_key = models.CharField(db_column="binanceSecretKey", max_length=64)
    user_binance = models.ForeignKey(
        UserBinance,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        db_column="userBinanceId",
    )
    is_key_active = models.BooleanField(db_column="isKeyActive")
    is_connected = models.BooleanField(db_column="isConnected", default=False)
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)

    class Meta:
        db_table = "UserApiKey"
        managed = False
