from rest_framework.views import APIView
from auths.serializers import CreateUserSerializer
from rest_framework.response import Response
from rest_framework import status
from auths.models import User
from rest_framework.permissions import AllowAny
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# 역직렬화
class RegisterView(APIView): # 목적: 사용자가 보낸 데이터를 저장하는 것
    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)
        # 시리얼라이저 안쓰면 하나하나 (리퀘스트 정보가 필요)
        # email = request.data['email']
        # username = request.data['username']
        # password = make_password(request.data['password']) # 암호화
        # phone = request.data['phone']
        # gender = request.data['gender']
        # nickname = request.data['nickname']

        # # 변수를 DB에 저장해보자
        # user = User(email=email, username=username, password=password, phone=phone, gender=gender, nickname=nickname)
        # user.save()
        # return Response('good')

# 직렬화
class AllUserView(APIView): # 목적: DB의 여러 사용자 데이터를 가져와서 응답으로 보내는 것
    def get(self, request):
        users = User.objects.all()
        serializer = CreateUserSerializer(users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

# 로그인 성공
class CheckLoginView(APIView):
    def get(self, request):
        return Response({"message": "로그인 성공"})

# 유저 존재 유무 확인
class UserExist(APIView):
    permission_classes = [AllowAny]  # 인증(액세스 토큰) 없이 접근 허용
    
    def post(self, request):
        email = request.data['email'] # 사용자가 요청 body에 email을 포함
        user = User.objects.filter(email=email).first()

        if user is None:
            return Response({"message": "not email found!"}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({"message": "User Exist"}, status=status.HTTP_200_OK)

# 사용자 한명의 데이터 가져오는 기능
class UserInfo(APIView):
    def post(self, request):
        user_id = request.auth.payload['user_id'] # user id JWT 토큰에서 추출
        user = User.objects.get(id=user_id) # db에서의 필드명: id / user_id로 User 객체 가져오기
        
        # 위의 user 정보를 가져오는 두 줄짜리 코드를 아래 한 줄로 표현할 수 있음
        #  따로 사용자 식별자를 추출할 필요 없이, request.user를 통해 현재 인증된 사용자를 바로 가져올 수 있음
        # user = request.user

        if user is None:
            return Response({"message": "user id {user_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            return Response({
                "data": {
                "username": user.username,
                "email": user.email
                }
            }, status=status.HTTP_200_OK)
        except Exception as e: # Python에서 발생할 수 있는 모든 예외의 기본 클래스
            return Response({"message": "{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# 유저 정보 수정        
class UserInfoUpdate(APIView):
    def patch(self, request): # 보통 put 보다 patch를 자주 사용
        user_id = request.auth.payload['user_id']
        user = User.objects.get(id=user_id)

        new_username = request.data['username']
        new_nickname = request.data['nickname']
        new_gender = request.data['gender']
        new_phone = request.data['phone']

        user.username = new_username
        user.nickname = new_nickname
        user.gender = new_gender
        user.phone = new_phone

        user.save() # DB 저장 (위까지만 하면 당연히 Response로만 불려져 오잖니)

        return Response({
                "message": "User info update success!!!!!!",
                "data": {
                    "email": user.email,
                    "username": user.username,
                    "nickname": user.nickname,
                    "gender": user.gender,
                    "phone": user.phone
                }
            }, status=status.HTTP_200_OK)
    
# 유저 삭제 
class UserDelete(APIView):
    def delete(self, request):
        user = request.user

        user.delete()

        return Response({
        "Message": "User info delete success!!!!",
        "data": {
            "email": user.email,
            "username": user.username
        }               
        }, status=status.HTTP_200_OK)

def home(request) :
    return render(request, "auths/home.html")

def check_login_status(request):
    return JsonResponse({
        "is_authenticated": request.user.is_authenticated,
        "username": request.user.username if request.user.is_authenticated else ""
    })