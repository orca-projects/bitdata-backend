from django.db import models


# 만들어진 유저 카카오테이블 가져와서 생성
class User(models.Model):
    id = models.AutoField(primary_key=True)  # serial은 AutoField에 매핑
    kakao_id = models.BigIntegerField(
        unique=True, db_column="kakaoId"
    )  # UUID 대신 BigIntegerField
    account_email = models.EmailField(
        max_length=255, db_column="accountEmail"
    )  # varchar(255)와 이메일 제약 조건
    name = models.CharField(max_length=255)  # varchar(255)
    phone_number = models.CharField(
        max_length=255, db_column="phoneNumber"
    )  # varchar(255)
    created_at = models.DateTimeField(
        auto_now_add=True, db_column="createdAt"
    )  # timestamp default now()
    deleted_at = models.DateTimeField(
        null=True, blank=True, db_column="deletedAt"
    )  # nullable timestamp

    class Meta:
        db_table = "User"  # 기존 테이블 이름 매핑
        managed = False  # Django가 이 테이블을 관리하지 않음 (기존 테이블이므로)

    def __str__(self):
        return f"{self.account_email} - {self.name}"
