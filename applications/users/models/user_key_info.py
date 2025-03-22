from django.db import models
from django.utils import timezone


class UserKeyInfo(models.Model):
    id = models.AutoField(primary_key=True)  # serial은 AutoField에 매핑
    kakao_id = models.ForeignKey(
        "User",  # User 모델과 외래 키로 연결
        to_field="kakao_id",  # 외래 키가 kakao_id임을 명시
        db_column="kakaoId",  # 데이터베이스 컬럼 이름 매핑
        on_delete=models.CASCADE,  # 부모(User) 삭제 시 동작 정의
    )
    binance_id = models.CharField(max_length=255, db_column="binanceId")  # varchar(255)
    created_at = models.DateTimeField(
        default=timezone.now, db_column="createdAt"
    )  # timestamp default now()
    is_connected = models.BooleanField(db_column="isConnected", default=False)
    is_key_active = models.BooleanField(db_column="isKeyActive", default=True)
    binance_api_key = models.CharField(
        max_length=255, db_column="binanceApiKey"
    )  # varchar(255)
    binance_secret_key = models.CharField(
        max_length=255, db_column="binanceSecretKey"
    )  # varchar(255)
    last_collected = models.DateTimeField(
        null=True, blank=True, db_column="lastCollected"
    )  # 추가된 컬럼

    class Meta:
        db_table = "UserKeyInfo"  # 기존 테이블 이름 매핑
        managed = False  # Django가 이 테이블을 관리하지 않음 (기존 테이블이므로)

    def __str__(self):
        return f"Binance ID: {self.binance_id}, Key Active: {self.is_key_active}"
