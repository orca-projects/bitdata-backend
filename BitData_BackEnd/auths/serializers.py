from rest_framework import serializers
from auths.models import User, UserKakao

class CreateUserSerializer(serializers.ModelSerializer) :
    class Meta :
        model = User # User 모델 사용
        fields = ['email', 'username', 'password', 'phone', 'gender', 'nickname'] # User 모델 내 필드

class CreateUserKakaoSerializer(serializers.ModelSerializer) :
    class Meta :
        model = UserKakao # UserKakao 모델 사용
        fields = ['kakaoId', 'accountEmail', 'name', 'phoneNumber']