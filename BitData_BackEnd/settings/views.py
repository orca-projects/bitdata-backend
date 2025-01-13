from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.contrib.sessions.models import Session
from auths.models import User, UserKakao, UserKeyInfo 
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# Class Name: GetProfileInfo
# Class 설명: 바이낸스에서 데이터를 수집하는 클래스스
# 작성자: 윤택한
# 수정자: 윤택한
# 생성 일자: 25.01.13(월)
# 수정 일자: 25.01.13(월)
class GetProfileInfo(APIView):
    def post(self, request):
        # Step 1: 세션 키 가져오기
        session_key = request.data.get('session_key')
        if not session_key:
            return JsonResponse({'오류': '세션 키가 누락되었습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # Step 2: 세션에서 사용자 정보 가져오기
        try:
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            user_info = session_data.get('kakao_user_info')

            if not user_info:
                return JsonResponse({'오류': '세션에서 사용자 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except Session.DoesNotExist:
            return JsonResponse({'오류': '유효하지 않은 세션 키입니다.'}, status=status.HTTP_404_NOT_FOUND)

        # Step 3: Kakao ID 기반 데이터 조회
        try:
            user_kakao = UserKakao.objects.get(kakaoId=user_info.get('kakaoId'))
            user_keys = UserKeyInfo.objects.get(kakaoId=user_kakao)
        except UserKakao.DoesNotExist:
            return JsonResponse({'오류': '데이터베이스에서 해당 카카오 ID를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        except UserKeyInfo.DoesNotExist:
            return JsonResponse({'오류': 'Binance 정보를 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        # Step 4: 데이터 가공
        name = self.mask_name(user_kakao.name)
        binance_id = user_keys.binanceId
        binance_api_key = self.mask_api_key(user_keys.binanceApiKey)

        # Step 5: 성공 응답 반환
        return JsonResponse({
            '이름': name,
            'Binance ID': binance_id,
            'Binance API Key': binance_api_key
        }, status=status.HTTP_200_OK)

    # 이름 마스킹 로직
    def mask_name(self, name):
        if len(name) == 1:
            return "*"  # 이름이 1자일 경우 전부 마스킹
        elif len(name) == 2:
            return f"{name[0]}*"  # 이름이 2자일 경우 2번째 글자 마스킹
        elif len(name) == 3:
            return f"{name[0]}*{name[2]}"  # 이름이 3자일 경우 2번째 글자 마스킹
        else:
            return f"{name[0]}{'*' * (len(name) - 2)}{name[-1]}"  # 4자 이상일 경우 첫글자, 마지막 글자 제외 마스킹

    # Binance API Key 마스킹 로직
    def mask_api_key(self, api_key):
        if len(api_key) < 2:
            return "*" * len(api_key)  # 길이가 짧을 경우 전부 마스킹
        return f"{api_key[0]}****{api_key[-1]}"  # 첫 글자, 마지막 글자 제외 나머지 마스킹