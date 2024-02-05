import os
import sys
import locale
import logging
from pathlib import Path

from dotenv import load_dotenv
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / '.env'

load_dotenv(dotenv_path=ENV_PATH)

SECRET_KEY = os.getenv('SECRET_KEY', '_')

PROJECT_NAME = os.getenv('PROJECT_NAME', 'TATNEFT TASK')

DEBUG = bool(int(os.getenv('DEBUG', 0)))

ALLOWED_HOSTS = ['*']

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'constance',
    'constance.backends.database',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'drf_yasg',
    'drf_standardized_errors',
    'django_celery_beat',
    'django_celery_results',
    'django_filters',

    'api.apps.ApiConfig',
    'core.apps.CoreConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S%Z',
    'DATETIME_INPUT_FORMAT': '%Y-%m-%d %H:%M:%S%Z',
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.ApiPagination',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'EXCEPTION_HANDLER': 'drf_standardized_errors.handler.exception_handler',
}

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

if os.getenv('SQL_PASSWORD'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'USER': os.getenv('SQL_USER', 'new_user'),
            'NAME': os.getenv('SQL_DATABASE', 'name'),
            'PASSWORD': os.getenv('SQL_PASSWORD', 'password'),
            'HOST': os.getenv('SQL_HOST', 'localhost'),
            'PORT': int(os.getenv('SQL_PORT', 5432)),
        },
    }

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'cache_table',
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-RU'

LANGUAGES = [
    ('ru', _('Русский')),
    ('en', _('English')),
]

TIME_ZONE = os.getenv('TIME_ZONE', 'Europe/Moscow')

USE_I18N = True

USE_TZ = True

locale.setlocale(locale.LC_ALL, 'ru_RU.UTF-8')

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

STATIC_ROOT = BASE_DIR / 'static'

MEDIA_ROOT = BASE_DIR / 'media'

ICONS_ROOT = MEDIA_ROOT / 'icons'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True

CONSTANCE_CONFIG = {
    'SOURCE_1': (os.getenv('URL_SOURCE_1', ''), 'ссылка на источник №1', str),
    'SOURCE_2': (os.getenv('URL_SOURCE_2', ''), 'ссылка на источник №2', str),
}

CONSTANCE_CONFIG_FIELDSETS = {
    '1. CONFIG': (
        'SOURCE_1',
        'SOURCE_2',
    ),
}

DRF_STANDARDIZED_ERRORS = {'EXCEPTION_FORMATTER_CLASS': 'api.exception_handler.Formatter'}

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')

REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))

REDIS_DB = int(os.getenv('REDIS_DB', 0))

CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}'

CELERY_RESULT_BACKEND = 'django-db'

CELERY_CACHE_BACKEND = 'django-cache'

CELERY_RESULT_EXTENDED = True

if 'test' in sys.argv:
    logging.getLogger('factory').setLevel('INFO')
    logging.getLogger('faker').setLevel('INFO')
