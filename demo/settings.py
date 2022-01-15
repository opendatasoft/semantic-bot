"""

Django settings for chatbot_app project.

Generated by 'django-admin startproject' using Django 1.11.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#BASE_DIR = "/semantic-bot/"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ["*"]
SECRET_KEY = 'change-me'
#ALLOWED_HOSTS = ["0.0.0.0","127.0.0.1","localhost"]

# To be defined in your local_settings
DATA_API_KEY = None
MAPPING_SERIALIZER = 'YARRRML'

# If True, all URIs (classes and properties) are used only if available (returns http code 200)
CHECK_URI_AVAILABILITY = False

# Set the minimal score for an URI to be used by the chatbot (see _custom_scoring function in utils/lov_ods_api)
MINIMAL_CHATBOT_SCORE = 700

# Set the number of records to retrieve
RECORD_NUMBER = 10

# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'chat',
    'webpack_loader'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'chatbot_app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "chat/templates")],
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

WSGI_APPLICATION = 'chatbot_app.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] [%(levelname)s] [%(module)s] %(message)s'
        }
    },
    'handlers': {
        'chatbot_results': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/chatbot_results.log',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'results_logger': {
            'handlers': ['chatbot_results'],
            'level': 'INFO',
            'propagate': False,
        }
    },
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

try:
    from .local_settings import *
except ImportError:
    pass

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'assets'),
)
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static_files')]

#STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
#STATIC_ROOT = '/semantic-bot/assets'
STATIC_URL = '/static/'
#STATIC_URL = 'http://dataverse.org.ua:8080/static/'
print(STATICFILES_DIRS)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundles/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}
