import datetime as dt
import os
from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = strtobool(os.getenv("DEBUG", "False"))

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "").split(",")


# Application definition

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "taggit",
    "rest_framework",
    "djoser",
    "django_filters",
    "dynamic_rest",
    "drf_yasg",
    "ordered_model",
    "corsheaders",
]

LOCAL_APPS = [
    "apps.users",
    "apps.utilities",
    "apps.courses",
    "apps.purchases",
    "apps.api",
    "apps.holder",
    "apps.bot",
    "apps.beautiful_soup",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "skillsup.urls"

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

WSGI_APPLICATION = "skillsup.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": os.getenv("POSTGRES_DB", "skillsup"),
        "USER": os.getenv("POSTGRES_USER", "skillsup"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD", "skillsup"),
        "HOST": os.getenv("POSTGRES_HOST", "localhost"),
        "PORT": int(os.getenv("POSTGRES_PORT", "5432")),
    }
}

AUTH_USER_MODEL = "users.User"

CACHE_REDIS_LOCATION = os.getenv("CACHE_REDIS_LOCATION")
if CACHE_REDIS_LOCATION:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.redis.RedisCache",
            "LOCATION": CACHE_REDIS_LOCATION,
        }
    }


# Password validation

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


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "static"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": ("rest_framework_simplejwt.authentication.JWTAuthentication",),
    "EXCEPTION_HANDLER": "apps.api.exceptions_handler.custom_exception_handler",
}

SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("Bearer",),
    "ACCESS_TOKEN_LIFETIME": dt.timedelta(days=365),
}

SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Для авторизации введите: Bearer Token", "in": "header"},
    },
}

DYNAMIC_REST = {
    "DEBUG": False,
    "ENABLE_BROWSABLE_API": True,
    "ENABLE_LINKS": False,
    "ENABLE_SERIALIZER_CACHE": True,
    "ENABLE_SERIALIZER_OPTIMIZATIONS": True,
    "DEFER_MANY_RELATIONS": False,
    "MAX_PAGE_SIZE": None,
    "PAGE_QUERY_PARAM": "page",
    "PAGE_SIZE": None,
    "PAGE_SIZE_QUERY_PARAM": "per_page",
    "ADDITIONAL_PRIMARY_RESOURCE_PREFIX": "+",
    "ENABLE_HOST_RELATIVE_LINKS": True,
}

CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 1 * 30
CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/2")

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 0))
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
CERTIFICATE_EMAIL_FROM = "Anton <anton.uranov@yandex.ru>"

BASE_PLATFORM_URL = os.getenv("BASE_PLATFORM_URL")

CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_WEBHOOK_TOKEN = os.getenv("TELEGRAM_WEBHOOK_TOKEN")
TELEGRAM_WEBHOOK_CALLBACK = os.getenv("TELEGRAM_WEBHOOK_CALLBACK")

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS", "https://api.skillsup.fun").split(",")

URL_VACANCY = os.getenv("URL_VACANCY")
