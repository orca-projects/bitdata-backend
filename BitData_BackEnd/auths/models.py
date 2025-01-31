from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150)
    phone = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    nickname = models.CharField(max_length=20, null=True, blank=True)
    # fullname = models.CharField(max_length=20, null=True, blank=True)
    # kakaoid = models.BigIntegerField(null=True, blank=True)

    USERNAME_FIELD='email' # 사용자의 고유한 식별자로 사용되는 필드
    REQUIRED_FIELDS=['username'] # 슈퍼유저를 생성할 때 프롬프트되는 추가 필드 목록

    def __str__(self):
        return f'{self.email} - {self.username}'

# 만들어진 유저 카카오테이블 가져와서 생성
class UserKakao(models.Model):
    id = models.AutoField(primary_key=True)  # serial은 AutoField에 매핑
    kakaoId = models.BigIntegerField(unique=True, db_column='kakaoId')  # UUID 대신 BigIntegerField
    accountEmail = models.EmailField(max_length=255, db_column='accountEmail')  # varchar(255)와 이메일 제약 조건
    name = models.CharField(max_length=255)  # varchar(255)
    phoneNumber = models.CharField(max_length=255, db_column='phoneNumber')  # varchar(255)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')  # timestamp default now()
    deletedAt = models.DateTimeField(null=True, blank=True, db_column='deletedAt')  # nullable timestamp

    class Meta:
        db_table = 'UserKakao'  # 기존 테이블 이름 매핑
        managed = False  # Django가 이 테이블을 관리하지 않음 (기존 테이블이므로)

    def __str__(self):
        return f'{self.accountEmail} - {self.name}'

class UserKeyInfo(models.Model):
    id = models.AutoField(primary_key=True)  # serial은 AutoField에 매핑
    kakaoId = models.ForeignKey(
        'UserKakao',  # UserKakao 모델과 외래 키로 연결
        to_field='kakaoId',  # 외래 키가 kakaoId임을 명시
        db_column='kakaoId',  # 데이터베이스 컬럼 이름 매핑
        on_delete=models.CASCADE  # 부모(UserKakao) 삭제 시 동작 정의
    )
    binanceId = models.CharField(max_length=255, db_column='binanceId')  # varchar(255)
    createdAt = models.DateTimeField(auto_now_add=True, db_column='createdAt')  # timestamp default now()
    isKeyActive = models.BooleanField(db_column='isKeyActive', default=True)
    binanceApiKey = models.CharField(max_length=255, db_column='binanceApiKey')  # varchar(255)
    binanceSecretKey = models.CharField(max_length=255, db_column='binanceSecretKey')  # varchar(255)

    class Meta:
        db_table = 'UserKeyInfo'  # 기존 테이블 이름 매핑
        managed = False  # Django가 이 테이블을 관리하지 않음 (기존 테이블이므로)

    def __str__(self):
        return f'Binance ID: {self.binanceId}, Key Active: {self.isKeyActive}'