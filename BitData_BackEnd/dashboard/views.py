from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.sessions.models import Session
from auths.models import UserKakao, UserKeyInfo
from binance.client import Client

# Class Name: GetBinanceTradeData
# Class 설명: session_key안에 있는 kakao Id 를 가지고 UserKeyInfo 테이블에서 Binance Api, Secret키를 가져와서 바이낸스 API 호출하는 API
# 작성자: 윤택한
# 수정자: 윤택한
# 생성 일자: 25.01.07(화)
# 수정 일자: 25.01.07(화)
class GetBinanceTradeData(APIView):
    def post(self, request):
        session_key = request.data.get('session_key')
        if not session_key:
            return JsonResponse({'error': 'Session key is required'}, status=400)

        try:
            # 세션에서 kakaoId 추출
            session = Session.objects.get(session_key=session_key)
            session_data = session.get_decoded()
            kakao_id = session_data.get('kakao_user_info', {}).get('kakaoId')
            if not kakao_id:
                return JsonResponse({'error': 'kakaoId not found in session'}, status=400)

            # API 키 및 Secret 키 가져오기
            user_key_info = UserKeyInfo.objects.filter(kakaoId=kakao_id).first()
            if not user_key_info:
                return JsonResponse({'error': 'API keys not found for the given kakaoId'}, status=404)

            # Binance 계정 정보 가져오기 -> 추후에 API만 변경하면 됨
            client = Client(user_key_info.binanceApiKey, user_key_info.binanceSecretKey)
            account_info = client.get_account()
            return JsonResponse({'account_info': account_info}, status=200)

        except Session.DoesNotExist:
            return JsonResponse({'error': 'Invalid session key'}, status=404)
        except Exception as e:
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=500)