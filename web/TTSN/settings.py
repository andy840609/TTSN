"""
Django settings for TTSN project.

Generated by 'django-admin startproject' using Django 3.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import os
from datetime import timedelta
from pathlib import Path

from gqlauth.settings_type import GqlAuthSettings, email_field

os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# print(BASE_DIR)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# admin RESTRICT
RESTRICT_ADMIN = os.environ.get('RESTRICT_ADMIN', '')
#ALLOWED_ADMIN_IPS=['140.109.82.44', '::1']
# ALLOWED_ADMIN_IP_RANGES=os.environ.get('ALLOWED_ADMIN_IP_RANGES',[])
ALLOWED_ADMIN_IP_RANGES = ['140.109.80.0/24', '140.109.81.0/24', '140.109.82.0/24']
RESTRICTED_APP_NAMES = os.environ.get('RESTRICTED_APP_NAMES', [])
TRUST_PRIVATE_IP = os.environ.get('TRUST_PRIVATE_IP', '')

# Application definition
INSTALLED_APPS = [
    # definition
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # modules pip
    'strawberry.django',
    # 'django_property_filter',
    "gqlauth",
    'corsheaders',
    'backend.apps.BackendConfig',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'admin_ip_restrictor.middleware.AdminIPRestrictorMiddleware',
]

ROOT_URLCONF = 'TTSN.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'frontend/dist'),
            os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'TTSN.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# 指定路由 > 為剛剛設置的檔案
# DATABASE_ROUTERS = ['專案名稱.檔案名稱.功能名稱']
DATABASE_ROUTERS = ['backend.database_router.DatabaseAppsRouter']
# 路由配對
DATABASE_APPS_MAPPING = {
    'cwb_report': 'cwb_report',
    # 'default': 'default',
}
# 接下來就是設定的部份，預先會定義一個default，當沒指定時就使用該DB
# 其餘部份就看使用的資料庫引擎及定義名稱、帳號、密碼等等
DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DBENGINE', ''),
        'NAME': os.environ.get('DBNAME', ''),
        'USER': os.environ.get('DBUSER', ''),
        'PASSWORD': os.environ.get('DBPASSWORD', ''),
        'HOST': os.environ.get('DBHOST', ''),
        'PORT': os.environ.get('DBPORT', ''),
        # "OPTIONS": {
        #     "init_command": "SET default_storage_engine=InnoDB;"
        # }
    }
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# AUTH_USER_MODEL = app_label.ModelName
# AUTH_USER_MODEL = 'backend.CustomUser'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "frontend/dist/static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

GQL_SERVER = os.environ.get("GRAPHQL_SERVER", "")
GQL_AUTH = GqlAuthSettings(
    LOGIN_REQUIRE_CAPTCHA=True,
    REGISTER_REQUIRE_CAPTCHA=True,
    LOGIN_FIELDS={email_field},
    # JWT
    # It means that you need to refresh every 5 mins (payload.exp)
    # and even you keep on refreshing token every 5 mins,
    # you will still be logout in 1 hours after the
    # first token has been issued (refreshExpiresIn).
    JWT_LONG_RUNNING_REFRESH_TOKEN=True,
    JWT_EXPIRATION_DELTA=timedelta(minutes=5),
    JWT_REFRESH_EXPIRATION_DELTA=timedelta(hours=1),
    # email templates
    EMAIL_TEMPLATE_ACTIVATION="email/activation_email.html",
    EMAIL_TEMPLATE_ACTIVATION_RESEND="email/activation_email.html",
    EMAIL_TEMPLATE_PASSWORD_SET="email/password_set_email.html",
    EMAIL_TEMPLATE_PASSWORD_RESET="email/password_reset_email.html",

)


# mutations.SendPasswordResetEmail 存在，所以需要
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('DJANGO_EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('DJANGO_EMAIL_PORT', '')
EMAIL_USE_SSL = bool(os.environ.get('DJANGO_EMAIL_USE_SSL', True))
EMAIL_HOST_USER = os.environ.get('DJANGO_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('DJANGO_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
MANAGERS = [('TEC Data Center', 'andy840609@earth.sinica.edu.tw'), ]

# CORS
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOWED_ORIGINS = ['http://localhost:8081','http://140.109.82.44:8000',]


# NTU APIs
NTU_HISTORY_KEY = os.environ.get('NTU_HISTORY_KEY', '')
NTU_REALTIME_KEY = os.environ.get('NTU_REALTIME_KEY', '')
NTU_RECORDS_KEY = os.environ.get('NTU_RECORDS_KEY', '')


# RECAPTCHA
GOOGLE_RECAPTCHA_SECRET = '6LdogwslAAAAABOS5m80HT5PFW-cmPajmIA-My0G'
GOOGLE_RECAPTCHA_SCORE = 0.58
