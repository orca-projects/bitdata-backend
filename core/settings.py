import os
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = True

ALLOWED_HOSTS = [
    "dev.bitdata.kr",
    "bitdata.kr",
]

ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

INSTALLED_APPS = [
    # Default Django applications
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party libraries and frameworks
    "rest_framework",
    "corsheaders",
    # Custom applications
    "applications.users",
    "applications.authentication",
    "applications.authorization",
    "applications.binance_api",
    "applications.transaction",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

if ENVIRONMENT == "development":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DEV_DB_NAME"),
            "USER": os.getenv("DEV_DB_USER"),
            "PASSWORD": os.getenv("DEV_DB_PASSWORD"),
            "HOST": os.getenv("DEV_DB_HOST"),
            "PORT": os.getenv("DEV_DB_PORT"),
        }
    }
elif ENVIRONMENT == "production":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("PROD_DB_NAME"),
            "USER": os.getenv("PROD_DB_USER"),
            "PASSWORD": os.getenv("PROD_DB_PASSWORD"),
            "HOST": os.getenv("PROD_DB_HOST"),
            "PORT": os.getenv("PROD_DB_PORT"),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

USE_I18N = True
LANGUAGE_CODE = "ko-kr"

USE_TZ = True
TIME_ZONE = "Asia/Seoul"

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_CREDENTIALS = True

ORIGINS = [
    "http://dev.bitdata.kr",
    "https://bitdata.kr",
]

CORS_ALLOWED_ORIGINS = ORIGINS
CSRF_TRUSTED_ORIGINS = ORIGINS

CSRF_COOKIE_NAME = "csrftoken"

SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_NAME = "bitdata_session_id"

# AUTH_USER_MODEL = "users.User"

KAKAO_REST_API_KEY = os.getenv("KAKAO_REST_API_KEY")
KAKAO_CLIENT_SECRET = os.getenv("KAKAO_CLIENT_SECRET")
if ENVIRONMENT == "development":
    KAKAO_REDIRECT_URL = "http://dev.bitdata.kr/callback"
elif ENVIRONMENT == "production":
    KAKAO_REDIRECT_URL = "https://bitdata.kr/callback"
KAKAO_REPONSE_TYPE = os.getenv("KAKAO_REPONSE_TYPE")

LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)  # logs 디렉토리가 없으면 생성

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{levelname}] {asctime} {module} | {message}",
            "style": "{",
        },
        "simple": {
            "format": "[{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "file_error": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "django_error.log",
            "formatter": "verbose",
        },
        "file_debug": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": LOG_DIR / "django_debug.log",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console", "file_error", "file_debug"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": True,
        },
        "django.request": {
            "handlers": ["console", "file_error"],
            "level": "ERROR",
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console", "file_debug"],
            "level": "DEBUG",
            "propagate": False,
        },
        "django.utils.autoreload": {
            "handlers": [],
            "level": "WARNING",
            "propagate": False,
        },
    },
}

BINANCE_DEFAULT_TIME = 1564588800001
