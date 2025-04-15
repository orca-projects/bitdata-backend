from django.db import models
from django.utils import timezone

from applications.users.models import User
from applications.transaction.models import PositionHistory


class Memo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    position_history = models.ForeignKey(
        PositionHistory, on_delete=models.CASCADE, db_column="positionHistoryId"
    )
    title = models.CharField(max_length=50)
    image = models.BinaryField()
    description = models.CharField(max_length=600)
    created_at = models.DateTimeField(db_column="createdAt", default=timezone.now)
    updated_at = models.DateTimeField(db_column="updatedAt", default=timezone.now)
    deleted_at = models.BooleanField(db_column="deletedAt")

    class Meta:
        db_table = "Memo"
        managed = False
