import random
import string
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
from django.http import HttpResponseRedirect
from rest_framework.exceptions import AuthenticationFailed
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Q  # 조건 검색에 사용할 수 있습니다
from auths.models import User, UserKakao, UserKeyInfo 
from django.contrib.sessions.backends.db import SessionStore
from django.middleware.csrf import get_token
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from binance.client import Client

# Create your views here.
def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})

# Class Name: GetKakaoLoginUrl
# Class 설명: 카카오톡 URL 생성후 반환 하는 클래스
# 작성자: 윤택한
# 수정자:
# 생성 일자: 24.12.15(금)
# 수정 일자: 
class GetKakaoLoginUrl(APIView):
    # Method Name: 
    # Method 설명:
    # 작성자:
    # 수정자:
    # 생성 일자:
    # 수정 일자: 
    def get(self, request):
        # 필수 파라미터
        client_id = settings.KAKAO_REST_API_KEY  # 카카오 REST API 키
        # redirect_uri = "http://localhost:5173/callback/"  # 로컬 개발용
        redirect_uri = "https://bitdata.kr/login/kakao/auths/callback"  # 실제 라이브 서버 배포용
        response_type = "code"  # 인가 코드 방식

        # 선택 파라미터
        state = ''.join(random.choices(string.ascii_letters + string.digits, k=16))  # CSRF 방어용
        request.session['oauth_state'] = state  # 세션에 저장하여 나중에 검증

        # 카카오 인증 URL 생성 (순서에 맞게 연결)
        kauth_url = (
            f"https://kauth.kakao.com/oauth/authorize?"
            f"response_type={response_type}"
            f"&redirect_uri={redirect_uri}"
            f"&state={state}"
            f"&client_id={client_id}"
            f"&scope="  # 빈값으로 처리, 나중에 필요한 scope 추가 가능
            f"&through_account=true"
        )

        # 최종 로그인 URL
        kakao_login_url = f"https://accounts.kakao.com/login/?continue={kauth_url.replace(':', '%3A').replace('/', '%2F').replace('?', '%3F').replace('&', '%26').replace('=', '%3D')}#login"
        return JsonResponse({"login_url": kakao_login_url})

# 인가코드와 state코드 받아와서 토큰 발급 및 유저 정보 조회
class KakaoLoginCallback(APIView):
    def post(self, request):
        # 1. 프론트에서 전달된 'code'와 'state' 받기
        # print("Request Data:", request.data)  # 전달된 데이터 로그 출력
        # print("Request Header:", request.headers)  # 전달된 데이터 로그 출력
        code = request.data.get('code')
        state = request.data.get('state')

        KAKAO_REST_API_KEY = settings.KAKAO_REST_API_KEY
        KAKAO_CLIENT_SECRET = settings.KAKAO_CLIENT_SECRET
        # REDIRECT_URI = "http://localhost:5173/callback/" # 로컬 개발 용
        REDIRECT_URI = "https://bitdata.kr/login/kakao/auths/callback" # 실제 라이브 용

        # token 받아오기
        data = {
            'grant_type': "authorization_code", 
            'client_id': KAKAO_REST_API_KEY,
            'redirect_uri': REDIRECT_URI,
            'client_secret': KAKAO_CLIENT_SECRET,
            'code': code
        }
        headers = {'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}

        token_response = requests.post('https://kauth.kakao.com/oauth/token', data = data, headers = headers)
        access_token = token_response.json().get('access_token')

        # print(token_response)
        # print(access_token)

        # token 검증하기
        headers = {"Authorization": f'Bearer {access_token}'}
        token_validate_response = requests.get('https://kapi.kakao.com/v1/user/access_token_info', headers = headers)
        # print(token_validate_response.json())

        # 사용자 정보 받아오기
        headers = {"Authorization": f'Bearer {access_token}', 'Content-type': 'application/x-www-form-urlencoded;charset=utf-8'}
        user_info_response = requests.post('https://kapi.kakao.com/v2/user/me', headers = headers)
        # print(user_info_response.json())

        user_info = user_info_response.json()

        # 4. 사용자 정보에서 이메일 확인
        # email = user_info.get('kakao_account', {}).get('email')
        # if not email:
        #     raise AuthenticationFailed("사용자 이메일 정보를 확인할 수 없습니다.")
                # 4. 사용자 정보에서 필요한 데이터 확인
        email = user_info.get('kakao_account', {}).get('email')
        kakao_id = user_info.get('id')
        phone_number = user_info.get('kakao_account', {}).get('phone_number')
        name = user_info.get('kakao_account', {}).get('name')

        if not email or not kakao_id or not phone_number or not name:
            raise AuthenticationFailed("필요한 사용자 정보를 확인할 수 없습니다.")

        # print(email)

        # 세션에 user_info 저장
        request.session['kakao_user_info'] = {
            'accountEmail': email,
            'kakaoId': kakao_id,
            'phoneNumber': phone_number,
            'name': name
        }
        request.session.save()  # 세션 강제 저장

        # print(request.session.session_key)
        # print(request.session['kakao_user_info'])  # 저장 후 바로 출력
        # print(request.session.items())

        # 세션 키를 응답으로 반환
        session_key = request.session.session_key

        # 5. 사용자 이메일을 기준으로 회원 여부 확인 (예시)
        is_member = self.check_if_user_exists(kakao_id, email, phone_number, name)
        has_binance_key = self.check_if_binance_key_exists(kakao_id)

        return JsonResponse({'is_member': is_member, 'session_key': session_key, 'hasBinanceKey': has_binance_key})

    def check_if_user_exists(self, kakao_id, email, phone_number, name):
        try:
            # 이메일이 존재하는지 확인
            # print(UserKakao.objects.filter(accountEmail=email).exists())
            print(UserKakao.objects.filter(
                kakaoId=kakao_id,
                accountEmail=email,
                phoneNumber=phone_number,
                name=name
            ).exists())
            return UserKakao.objects.filter(
                kakaoId=kakao_id,
                accountEmail=email,
                phoneNumber=phone_number,
                name=name
            ).exists()
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return False

    def check_if_binance_key_exists(self, kakao_id):
        try:
            # kakaoId로 필터링하여 binanceApiKey와 binanceSecretKey가 모두 존재하는지 확인
            exists = UserKeyInfo.objects.filter(
                kakaoId=kakao_id,  # 해당 kakaoId로 필터링
            ).exclude(
                binanceApiKey__isnull=True
            ).exclude(
                binanceSecretKey__isnull=True
            ).exists()
            return exists
        except Exception as e:
            print(f"DB 조회 오류: {str(e)}")
            return False

# 빗데이터 동의 페이지 이후 회원 저장 시키는 로직 추후에 serializer사용할 예정
class ConsentView(APIView):
    def post(self, request):
        # 클라이언트로부터 세션 키 받기
        session_key = request.data.get('session_key')
        if not session_key:
            return JsonResponse({'error': 'Session key is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # 세션 데이터베이스에서 세션 객체 가져오기
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()

            # 세션에서 사용자 정보 가져오기
            user_info = session_data.get('kakao_user_info')
            print(user_info)
            if not user_info:
                return JsonResponse({'error': 'User info not found in session'}, status=status.HTTP_404_NOT_FOUND)

            # 각 정보 가져오기
            email = user_info.get('accountEmail')
            phone = user_info.get('phoneNumber')
            name = user_info.get('name')
            id = user_info.get('kakaoId')

            try:
                user = UserKakao.objects.create(
                    accountEmail=email,
                    phoneNumber=phone,
                    name=name,
                    kakaoId=id,
                )
                user.save()
            except Exception as e:
                return JsonResponse({'message': f'사용자 저장 실패: {str(e)}'}, status=500)
            return JsonResponse({'message': '사용자 정보 조회 성공', 'user_info': user_info})
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'Invalid session key'}, status=404)
        
# Class Name: SaveBinanceKeys
# Class 설명: 바이낸스 시크릿, API 키를 저장하는 클래스
# 작성자: 윤택한
# 수정자: 윤택한
# 생성 일자: 24.12.15(일)
# 수정 일자: 25.01.13(월)
class SaveBinanceKeys(APIView) :
    def post(self, request) :
        # Step 1: 필수 필드 검증
        required_fields = {
            'session_key': request.data.get('session_key'),
            'apiKey': request.data.get('api_key'),
            'secretKey': request.data.get('secret_key')
        }

        missing_fields = [key for key, value in required_fields.items() if not value]
        
        if missing_fields:
            return JsonResponse(
                {'오류': f"필수 입력 항목이 누락되었습니다: {', '.join(missing_fields)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        session_key = required_fields['session_key']
        binance_api_key = required_fields['apiKey']
        binance_secret_key = required_fields['secretKey']

        if not session_key:
            return JsonResponse({'error': 'Session key가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if not binance_api_key:
            return JsonResponse({'error': 'Binance Api key가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        if not binance_secret_key:
            return JsonResponse({'error': 'Binance Seceret key가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Step 2: 세션에서 사용자 정보 가져오기
        try:
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            user_info = session_data.get('kakao_user_info')

            if not user_info:
                return JsonResponse(
                    {'오류': '세션에서 사용자 정보를 찾을 수 없습니다.'},
                    status=status.HTTP_404_NOT_FOUND
                )
        except Session.DoesNotExist:
            return JsonResponse({'오류': '유효하지 않은 세션 키입니다.'}, status=status.HTTP_404_NOT_FOUND)

        # Step 3: Kakao ID 기반 사용자 확인
        try:
            user_kakao = UserKakao.objects.get(kakaoId=user_info.get('kakaoId'))
        except UserKakao.DoesNotExist:
            return JsonResponse({'오류': '데이터베이스에서 해당 카카오 ID를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # Step 4: Binance API Key와 Secret Key 저장
        try:
            user_key_info, created = UserKeyInfo.objects.update_or_create(
                kakaoId=user_kakao,
                defaults={
                    'binanceApiKey': binance_api_key,
                    'binanceSecretKey': binance_secret_key
                }
            )
            user_key_info.save()
        except Exception as e:
            return JsonResponse({'오류': f'바이낸스 키 저장 중 오류가 발생했습니다: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 성공 반환
        return JsonResponse({'메시지': '바이낸스 키가 성공적으로 저장되었습니다.'}, status=status.HTTP_200_OK)

# Class Name: CollectDataFromBinance
# Class 설명: 바이낸스에서 데이터를 수집하는 클래스스
# 작성자: 윤택한
# 수정자: 윤택한
# 생성 일자: 25.01.13(월)
# 수정 일자: 25.01.13(월)
class CollectDataFromBinance(APIView):
    def post(self, request):
        # Step 1: 세션 키 가져오기
        session_key = request.data.get('session_key')
        if not session_key:
            return JsonResponse({'result': 'F', 'error': 'Session key 가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: 세션 객체 디코드
        try:
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
        except Session.DoesNotExist:
            return JsonResponse({'result': 'F', 'error': 'session key가 일치하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # Step 3: 사용자 정보 확인
        user_info = session_data.get('kakao_user_info')
        if not user_info:
            return JsonResponse({'result': 'F', 'error': 'User info가 세션에 존재하지 않습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # Step 4: Kakao ID 기반 데이터 가져오기
        try:
            user_kakao = UserKakao.objects.get(kakaoId=user_info.get('kakaoId'))
            binance_api_key = UserKeyInfo.objects.get(kakaoId=user_kakao).binanceApiKey
            binance_secret_key = UserKeyInfo.objects.get(kakaoId=user_kakao).binanceSecretKey
        except UserKakao.DoesNotExist:
            return JsonResponse({'result': 'F', 'error': 'User Kakao ID가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except UserKeyInfo.DoesNotExist:
            return JsonResponse({'result': 'F', 'error': 'Binance API keys가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # Step 5: Binance UID 가져오기
        binance_uid = self.get_binance_uid(binance_api_key, binance_secret_key)
        if not binance_uid:
            return JsonResponse({'result': 'F', 'error': 'Binance UID를 가져오는데 실패하였습니다다. API Keys를 확인해주세요요.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 6: UID 저장
        try:
            user_key_info, created = UserKeyInfo.objects.update_or_create(
                kakaoId=user_kakao,
                defaults={'binanceId': binance_uid}
            )
            user_key_info.save()
        except Exception as e:
            return JsonResponse({'result': 'F', 'error': f'Binance UID를 저장하는데 실패했습니다다: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # 성공 반환
        return JsonResponse({'result': 'T'}, status=status.HTTP_200_OK)
    # Function Name: get_binance_uid
    # Function 설명: 바이낸스에서 UID 가져오기기
    # 작성자: 윤택한
    # 수정자: 윤택한
    # 생성 일자: 25.01.13(월)
    # 수정 일자: 25.01.13(월)
    def get_binance_uid(self, api_key, secret_key):
        try:
            client = Client(api_key, secret_key)
            account_info = client.get_account()
            return account_info.get('uid')  # UID 반환
        except Exception as e:
            print(f"Error fetching Binance UID: {e}")
            return None