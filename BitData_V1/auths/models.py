from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
  email = models.EmailField(max_length=255, unique=True)
  username = models.CharField(max_length=150)
  phone = models.CharField(max_length=30, null=True, blank=True)
  gender = models.CharField(max_length=10, null=True, blank=True)
  nickname = models.CharField(max_length=20, null=True, blank=True)

  USERNAME_FIELD='email' # 사용자의 고유한 식별자로 사용되는 필드
  REQUIRED_FIELDS=['username'] # 슈퍼유저를 생성할 때 프롬프트되는 추가 필드 목록

  def __str__(self):
    return f'{self.email} - {self.username}'