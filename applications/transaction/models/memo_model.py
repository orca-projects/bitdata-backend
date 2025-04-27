from django.db import models
from django.utils import timezone


class Memo(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.BigIntegerField(db_column="userId")
    position_history_id = models.BigIntegerField(db_column="positionHistoryId")
    title = models.CharField(max_length=50)
    image = models.BinaryField()
    description = models.CharField(max_length=600)
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)
    is_deleted = models.BooleanField(db_column="isDeleted", default=False)

    class Meta:
        db_table = "Memo"
        managed = False
