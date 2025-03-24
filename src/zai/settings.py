"""
Django settings for zai project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SERVER_NAME = os.environ.get("SERVER_NAME", "")
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-dtn#-z4y+mdep3um6#&c!c(tn7g7k^pd6udoqa3w8kqr=k+&$p"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "True") == "True"

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://127.0.0.1:8888",
    f"https://{SERVER_NAME}",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "graphene_django",
    "debug_toolbar",
    "corsheaders",
    "django_filters",
    "graphql_jwt.refresh_token.apps.RefreshTokenConfig",
    "users.apps.UsersConfig",
    "app_auth.apps.AuthConfig",
    "phonebook.apps.PhonebookConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "api.middleware.CustomSessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

GRAPHENE = {
    "SCHEMA": "api.graphql.schema",
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
]

ROOT_URLCONF = "zai.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "zai.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "postgres"),
        "USER": os.environ.get("DB_USER", "postgres"),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": os.environ.get("DB_PORT", "1303"),
    },
}

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "cache_table",
    }
}

AUTH_USER_MODEL = "users.User"

GRAPHQL_JWT = {
    "JWT_COOKIE_NAME": "zai_access-token",
    "JWT_REFRESH_TOKEN_COOKIE_NAME": "zai_refresh-token",
    "JWT_VERIFY_EXPIRATION": True,
    "JWT_HIDE_TOKEN_FIELDS": True,
    "JWT_COOKIE_SECURE": DEBUG,
    "JWT_COOKIE_SAMESITE": "Lax",
    "JWT_LONG_RUNNING_REFRESH_TOKEN": True,
    "JWT_EXPIRATION_DELTA": timedelta(hours=1),
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATICFILES_DIRS = [
    ("zai", BASE_DIR / "assets"),
]
STATIC_ROOT = BASE_DIR / "static"
STATIC_URL = os.environ.get("STATIC_URL", "static/")
WHITENOISE_STATIC_PREFIX = os.environ.get("WHITENOISE_STATIC_PREFIX", STATIC_URL)
FORCE_SCRIPT_NAME = os.environ.get("FORCE_SCRIPT_NAME", None)

DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": lambda request: DEBUG}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "time=%(asctime)s level=%(levelname)s location=%(name)s.%(funcName)s msg=%(message)s",
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
        "app_auth": {"handlers": ["console"], "level": "INFO"},
        "users": {"handlers": ["console"], "level": "INFO"},
        "phonebook": {"handlers": ["console"], "level": "INFO"},
        "api": {"handlers": ["console"], "level": "INFO"},
        "graphql.execution": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
