"""
Django settings for mygarage project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

import environ
from django.core.management.utils import get_random_secret_key

env = environ.Env()
# reading .env file
environ.Env.read_env()

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# offline setup
# PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')
# PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'accounts/static/js', 'serviceworker.js')
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("DJANGO_ALLOWED_HOSTS", "127.0.0.1").split(",")
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms', 'inflect', 'num2words',
    'customer', 'accounts', 'supplier', 'payments',
    'family', 'category', 'stock', 'product', 'buyorder',
    'billing', 'sellorder', 'vehicule', 'rdv', 'caisse',
    'discount', 'services', 'mathfilters', 'bank', 'employee',
    'rest_framework', 'django_filters',
    # 'pwa'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # 'django.middleware.cache.UpdateCacheMiddleware',  # new
    'django.middleware.common.CommonMiddleware',
    #  'django.middleware.cache.FetchFromCacheMiddleware',  # new
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SECURE_SSL_REDIRECT = False

ROOT_URLCONF = 'mygarage.urls'

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

WSGI_APPLICATION = 'mygarage.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ.get('DBNAME'),
            'USER': os.environ.get('DBUSER'),
            'PASSWORD': os.environ.get('DBPASSWORD'),
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
# Heroku Configuration
# import dj_database_url

# db_from_env = dj_database_url.config(conn_max_age=900)
# DATABASES['default'].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = ' '

# how the translation is done
# 1- django-admin makemessages -l fr or ar or any other language
# 2- django-admin compilemessages
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]

LANGUAGES = [
    ('en', 'English'),
    ('fr', 'Francais'),
    ('ar', 'Arabic'),

]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
# Heroku Config
if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATIC_URL = '/static/'

    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static')
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static/')
    STATIC_URL = '/static/'

# CSS LOCATION
CSS_LOCATION = os.path.join(BASE_DIR, 'static/')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
MEDIA_URL = '/media/'

# URLS
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'accounts:login'


# OFFLINE
# PWA_APP_NAME = 'My App'
# PWA_APP_DESCRIPTION = "My app description"
# PWA_APP_THEME_COLOR = '#0A0302'
# PWA_APP_BACKGROUND_COLOR = '#ffffff'
# PWA_APP_DISPLAY = 'standalone'
# PWA_APP_SCOPE = '/'
# PWA_APP_ORIENTATION = 'any'
# PWA_APP_START_URL = '/'
# PWA_APP_STATUS_BAR_COLOR = 'default'
# PWA_APP_ICONS = [
#     {
#         'src': '/static/img/no_image.png',
#         'sizes': '160x160'
#     }
# ]
# PWA_APP_ICONS_APPLE = [
#     {
#         'src': '/static/img/no_image.png',
#         'sizes': '160x160'
#     }
# ]
# PWA_APP_SPLASH_SCREEN = [
#     {
#         'src': '/static/img/no_image.png',
#         'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
#     }
# ]
# PWA_APP_DIR = 'ltr'
# PWA_APP_LANG = 'en-US'
#
# # Cache setting
# CACHE_MIDDLEWARE_ALIAS = 'default'  # which cache alias to use
# CACHE_MIDDLEWARE_SECONDS = 600  # number of seconds to cache a page for (TTL)
# CACHE_MIDDLEWARE_KEY_PREFIX = ''  # should be used if the cache is shared across multiple sites that use the same Django instance
#
#
# def get_cache():
#     import os
#     try:
#         servers = os.environ['mc2.dev.ec2.memcachier.com:11211']
#         username = os.environ['8D55B5']
#         password = os.environ['AA0847F049CA8AE8362D63E0B0829916']
#         return {
#             'default': {
#                 'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
#                 # TIMEOUT is not the connection timeout! It's the default expiration
#                 # timeout that should be applied to keys! Setting it to `None`
#                 # disables expiration.
#                 'TIMEOUT': None,
#                 'LOCATION': servers,
#                 'OPTIONS': {
#                     'binary': True,
#                     'username': username,
#                     'password': password,
#                     'behaviors': {
#                         # Enable faster IO
#                         'no_block': True,
#                         'tcp_nodelay': True,
#                         # Keep connection alive
#                         'tcp_keepalive': True,
#                         # Timeout settings
#                         'connect_timeout': 2000,  # ms
#                         'send_timeout': 750 * 1000,  # us
#                         'receive_timeout': 750 * 1000,  # us
#                         '_poll_timeout': 2000,  # ms
#                         # Better failover
#                         'ketama': True,
#                         'remove_failed': 1,
#                         'retry_timeout': 2,
#                         'dead_timeout': 30,
#                     }
#                 }
#             }
#         }
#     except:
#         return {
#             'default': {
#                 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'
#             }
#         }
#
#
# CACHES = get_cache()
