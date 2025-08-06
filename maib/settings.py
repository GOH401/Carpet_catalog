"""
Django settings for maib project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# --- 🔹 1. Базовая настройка путей
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 🔹 2. Загружаем переменные окружения ДО любых вызовов os.environ.get()
load_dotenv(BASE_DIR / ".env")

# --- 🔹 3. Cloudinary конфигурация (API ключи берутся из .env)
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# --- 🔹 4. Основные настройки Django
SECRET_KEY = 'django-insecure-(5kz$0m7qyj25j$2*d4+ml#vc@$r(1oi_poydg94-bewn*g(j%'
DEBUG = True

ALLOWED_HOSTS = [
    'catalognew-production.up.railway.app',
    '127.0.0.1',
    'localhost'
]

# доверяем запросам с этого origin (Django 4.0+ требует полный URL с https://)
CSRF_TRUSTED_ORIGINS = [
    'https://catalognew-production.up.railway.app',
]

# если вы сидите за прокси (Railway), чтобы правильно определялась схема HTTPS:
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- 🔹 5. Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'maib.catalog',
    'maib.logistics',
    'widget_tweaks',
    'cloudinary',
    'cloudinary_storage',
]

# --- 🔹 6. Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',            # ← добавлено для раздачи статики
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'maib.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'maib.catalog.context_processors.collections_list',
            ],
        },
    },
]

WSGI_APPLICATION = 'maib.wsgi.application'

# --- 🔹 7. База данных (Railway)
DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://postgres:ueSBInEYPSeZkOPPDanzEWAxvLyvPQjv@switchyard.proxy.rlwy.net:49336/railway",
        conn_max_age=600
    )
}

# --- 🔹 8. Парольные валидаторы
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- 🔹 9. Интернационализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- 🔹 10. Статика и медиа

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # сюда будет собираться collectstatic
STATICFILES_DIRS = [
    BASE_DIR / "maib" / "static",
]
# WhiteNoise storage backend
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = '/'

# --- 🔹 11. Cloudinary Storage
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
    'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
}

# --- 🔹 12. Auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
