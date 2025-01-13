from django.urls import path
from settings.views import GetProfileInfo
from . import views

# from auths.views import 
urlpatterns = [
    path('getprofile/', GetProfileInfo.as_view(), name='get-profile-info')
]