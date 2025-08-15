"""
Django settings for maib project.
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")





SECRET_KEY = 'django-insecure-(5kz$0m7qyj25j$2*d4+ml#vc@$r(1oi_poydg94-bewn*g(j%'
DEBUG = True

ALLOWED_HOSTS = [
    'catalognew-production.up.railway.app',
    '127.0.0.1',
    'localhost'
]

CSRF_TRUSTED_ORIGINS = [
    'https://catalognew-production.up.railway.app',
]

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

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

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
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


DATABASES = {
    'default': dj_database_url.parse(
        "postgresql://postgres:ueSBInEYPSeZkOPPDanzEWAxvLyvPQjv@switchyard.proxy.rlwy.net:49336/railway",
        conn_max_age=600
    )
}


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True



STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'   # сюда будет собираться collectstatic
STATICFILES_DIRS = [
    BASE_DIR / "maib" / "static",
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = '/'

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
SUPABASE_PUBLIC_BASE = "https://duzoqsgaglqlazqrpoun.supabase.co/storage/v1/object/public/balcatalog/public"
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET", "balcatalog")
SUPABASE_FOLDER = os.getenv("SUPABASE_FOLDER", "public")
SUPABASE_PUBLIC_BASE = f"{SUPABASE_URL}/storage/v1/object/public/{SUPABASE_BUCKET}/{SUPABASE_FOLDER}"