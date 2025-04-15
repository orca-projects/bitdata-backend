from django.db import models
from django.utils import timezone


class User(models.Model):
    kakao_uid = models.BigIntegerField(db_column="kakaoUid", unique=True)
    account_email = models.CharField(db_column="accountEmail", max_length=100)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(db_column="phoneNumber", max_length=20)
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)
    deleted_at = models.BooleanField(db_column="deletedAt")

    class Meta:
        db_table = "User"
        managed = False
