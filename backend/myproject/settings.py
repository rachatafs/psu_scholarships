from pathlib import Path
import os

# แก้ BASE_DIR ให้ชี้ขึ้นไป 3 ระดับ
# เดิม: backend/myproject/ → parent.parent = backend/
# ใหม่: backend/myproject/ → parent.parent.parent = psu_scholarships/
BASE_DIR = Path(__file__).resolve().parent.parent.parent  # ← แก้จุดที่ 1

SECRET_KEY = 'django-insecure-10%5u*@225j+m!k75bb*h$yv+g#uet%_o61^d+&dq9ob2pfiqk'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'scholarships',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'myproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend' / 'templates'],  # ← แก้จุดที่ 2
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'myproject.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'backend' / 'db.sqlite3',  # ← แก้จุดที่ 3
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

from django.utils.translation import gettext_lazy as _

LANGUAGE_CODE = 'th'

LANGUAGES = [
    ('th', _('Thai')),
    ('en', _('English')),
]

USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_ZONE = 'Asia/Bangkok'

LOCALE_PATHS = [
    BASE_DIR / 'backend' / 'locale',  # ← แก้จุดที่ 4
]

# =============================================
# STATIC & MEDIA
# =============================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'frontend' / 'static']  

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'frontend' / 'media'  

# =============================================
# AUTH
# =============================================
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'