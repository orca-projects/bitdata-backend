from django.contrib import admin
from auths.models import User

# admin.site.register로 User 모델을 관리자(admin 페이지)에 등록
admin.site.register(User)