from django.urls import path
from auths.views import RegisterView, AllUserView, CheckLoginView, UserExist, UserInfo, UserInfoUpdate, UserDelete
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)

urlpatterns = [
    path('users/', AllUserView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('islogin/', CheckLoginView.as_view()),
    path('userexist/', UserExist.as_view()),
    path('userinfo/', UserInfo.as_view()),
    path('userinfoupdate/', UserInfoUpdate.as_view()),
    path('userdelete/', UserDelete.as_view()),
]