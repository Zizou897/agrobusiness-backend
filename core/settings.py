from datetime import timedelta
import os
from pathlib import Path
import environ
from firebase_admin import initialize_app
from firebase_admin import credentials

# Reading .env file
env = environ.Env()
environ.Env.read_env()

# Define the application directory
ROOT_DIR = environ.Path(__file__) - 2
CORE_DIR = ROOT_DIR.path("core")

BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "0.0.0.0",
    "localhost",
    "services.devslabel.com",
    "31.220.72.160",
    "webadmin.devslabel.com",
]

# Application definition
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "celery",
    "django_celery_results",
    "drf_standardized_errors",
    "drf_spectacular",
    "drf_spectacular_sidecar",
    "templated_email",
    "fcm_django",
    "ckeditor",
    "corsheaders",
    "django_celery_beat",
    "cities_light",
    "account",
    "authentication",
    "advert",
    "news",
    "notification",
    "settings",
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
        "DIRS": [os.path.join(BASE_DIR, "templates")],
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

SERVER_EMAIL = env.str("SERVER_EMAIL")

# Database

DATABASES = {
    "default": {
        # "NAME": BASE_DIR / "db.sqlite3",
        "ENGINE": env.str("DB_ENGINE_PROD"),
        "HOST": env.str("DB_HOST"),
        "NAME": env.str("DB_NAME"),
        "USER": env.str("DB_USER"),
        "PASSWORD": env.str("DB_PASSWORD"),
        "PORT": env.int("DB_PORT"),
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://localhost:4100",
    "http://31.220.72.160",
    "https://services.devslabel.com",
    "https://webadmin.devslabel.com",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:8000",
    "http://31.220.72.160",
    "https://services.devslabel.com",
    "https://webadmin.devslabel.com",
]

CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
)

DATE_INPUT_FORMATS = ["%d-%m-%Y"]

AUTH_USER_MODEL = "authentication.User"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_CACHE_BACKEND": "django_redis.cache.RedisCache",
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler",
    "DATETIME_FORMAT": "%d-%m-%Y %H:%M:%S",
    "DATE_FORMAT": "%d-%m-%Y",
}


# DJANGO REST FRAMEWORK SPECTACULAR
SPECTACULAR_SETTINGS = {
    "TITLE": "AGROBUSINESS API",
    "DESCRIPTION": "Agrobusiness description",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SCHEMA_PATH_PREFIX": r"/api/v[0-9]",
}

# DJANGO SIMPLE JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(weeks=8),
    "REFRESH_TOKEN_LIFETIME": timedelta(weeks=9),
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
}

# DJANGO CITIES LIGHT
CITIES_LIGHT_TRANSLATION_LANGUAGES = ["fr"]
CITIES_CITY_MODEL = "cities_light.City"
CITIES_COUNTRY_MODEL = "cities_light.Country"

# EMAIL CONFIGURATION
EMAIL_BACKEND = env.str("EMAIL_BACKEND_PROD")
EMAIL_HOST = env.str("EMAIL_HOST_PROD")
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER_PROD")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD_PROD")
EMAIL_PORT = env.int("EMAIL_PORT_PROD")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL")
EMAIL_USE_TLS = False

# CELERY SETTINGS
CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
CELERY_RESULT_BACKEND = "django-db"
CELERY_CACHE_BACKEND = "django-cache"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers.DatabaseScheduler"

FCM_DJANGO_SETTINGS = {
    "APP_VERBOSE_NAME": env.str("APP_VERBOSE_NAME"),
    "FCM_SERVER_KEY": env.str("FCM_SERVER_KEY"),
    "ONE_DEVICE_PER_USER": env.bool("ONE_DEVICE_PER_USER"),
    "DELETE_INACTIVE_DEVICES": env.bool("DELETE_INACTIVE_DEVICES"),
    "UPDATE_ON_DUPLICATE_REG_ID": env.bool("UPDATE_ON_DUPLICATE_REG_ID"),
}

cred = credentials.Certificate(
    {
        "type": env.str("FIREBASE_ACCOUNT_TYPE"),
        "project_id": env.str("FIREBASE_PROJECT_ID"),
        "private_key_id": env.str("FIREBASE_PRIVATE_KEY_ID"),
        "private_key": env.str("FIREBASE_PRIVATE_KEY").replace(r"\n", "\n"),
        "client_email": env.str("FIREBASE_CLIENT_EMAIL"),
        "client_id": env.str("FIREBASE_CLIENT_ID"),
        "auth_uri": env.str("FIREBASE_AUTH_URI"),
        "token_uri": env.str("FIREBASE_TOKEN_URI"),
        "auth_provider_x509_cert_url": env.str("FIREBASE_AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": env.str("FIREBASE_CLIENT_X509_CERT_URL"),
    }
)

FIREBASE_APP = initialize_app(cred)

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "fr-fr"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(ROOT_DIR, "static")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
