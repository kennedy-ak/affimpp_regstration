"""
Django settings for affimpp_regstration project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# .env
SECRET_KEY='django-insecure-@y*6bkj#w@6&$lzy!s=_v&f7=)7@6sff@mq4i#v%8l&7p+3*&@'
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG=True
DEBUG = os.environ.get('DEBUG',"False").lower == "true"

ALLOWED_HOSTS= ["*"]
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(" ")

# Application definition

INSTALLED_APPS = [
    "base",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
  
]

MIDDLEWARE = [
 
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'affimpp_regstration.urls'

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

WSGI_APPLICATION = 'affimpp_regstration.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field
import os
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


ADMIN_LOGIN_URL = '/admin-login/'

LOGIN_REDIRECT_URL = 'student_dashboard'

LOGOUT_REDIRECT_URL = 'landing'
# Whitenoise settings for serving static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_PORT = 465
EMAIL_USE_SSL = True
  # Only use one: SSL or TLS
# EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'kennedyakogokweku@gmail.com'
EMAIL_HOST_PASSWORD = 'fsjvbeaseumsruzm'  # Use the App Password here
# mNotify Key

MNOTIFY_API_KEY = "qqYaIprq4RZ25q9JENdRqQbKZ"

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# PAYSTACK_SECRET_KEY= "sk_live_e08e6b8e8297451355dd0c83ab46de79047603a2"
# PAYSTACK_PUBLIC_KEY = "pk_live_f1a7cd719ecbc0c5890ad4178cdf0f5f0ce8a2e3"


PAYSTACK_SECRET_KEY = "sk_test_e5548034f1f6577dd88ca6a86599c15cedfee966"
PAYSTACK_PUBLIC_KEY = "pk_test_e463508717d557cbecd7a2e6024fb1decdeffa8f"

