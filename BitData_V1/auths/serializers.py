from rest_framework import serializers
from auths.models import User

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User # User 모델 사용
        fields=['email', 'username', 'password', 'phone', 'gender', 'nickname'] # User 모델 내 필드

    # 실제로 DB에 새로운 유저 객체를 저장하는 메서드
    def create(self, validated_data):
        # validated_data에서 password 키를 꺼내와서 password 변수에 저장
        # 비밀번호는 암호화해서 저장해야 하기 때문에 따로 뺌
        password = validated_data.pop('password', None)
        # 유저 모델을 만들기 위한 코드
        instance = self.Meta.model(**validated_data)
        print(f'instance: {instance}') # instance: user4@user.com - user4
        if password is not None: #password가 있으면 아래의 코드를 실행/비밀번호가 없으면 저장 X
            instance.set_password(password)
        # 만들어진 유저 객체를 DB에 저장. 아래 코드가 실행되면 새 유저가 DB에 기록됨
            instance.save()
            # 마지막으로 새로 만들어진 유저 객체(instance)를 반환
            return instance