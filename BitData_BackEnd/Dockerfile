# Dockerfile
# Python 3.12 베이스 이미지 사용
FROM python:3.12

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 복사 및 설치
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . /app/

# Django에서 사용할 포트 설정
EXPOSE 8080

# Gunicorn을 사용하여 Django 실행
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "bitdata_core.wsgi:application"]