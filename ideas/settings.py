"""
Django settings for ideas project.

Generated by 'django-admin startproject' using Django 4.2.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from datetime import timedelta
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from decouple import config
from ideasApi.log_handlers import MinimalEmailHandler



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ['http://3.129.20.16:8000/','http://localhost']
# Application definition

REQUEST_THRESHOLD = 1000

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ideasApi.apps.IdeasapiConfig',
    'import_export',
    'user_app.apps.UserAppConfig',
    'ckeditor',
    'rest_framework',
    'rest_framework.authtoken',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ideasApi.middleware.APILoggingMiddleware', 
    'user_app.middleware.APILoggingMiddleware', 
    'ideasApi.middleware.ProxyDetectionMiddleware',
    'ideasApi.request_count.RequestCountMiddleware',  
#     'user_app.middleware.ProxyDetectionMiddleware',
]

ROOT_URLCONF = 'ideas.urls'

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

WSGI_APPLICATION = 'ideas.wsgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / config('DATABASE')
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': config('DB_NAME'),    # Your MySQL database name
#         'USER': config('DB_USER'),      # Your MySQL user
#         'PASSWORD': config('DB_PASSWORD'),  # Your MySQL user's password
#         'HOST': '127.0.0.1',       # MySQL host (use IP or hostname if not local)
#         'PORT': '3306',            # MySQL port
#     }
# }




# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Los_Angeles'

USE_I18N = True

USE_TZ = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  # Your SMTP server's host
EMAIL_PORT = 587  # SMTP port (usually 587 for TLS)
EMAIL_USE_TLS = True  # Use TLS for secure connection
EMAIL_USE_SSL = False  # Set to True if using SSL instead of TLS
EMAIL_HOST_USER = config('EMAIL')  # Your email username
EMAIL_HOST_PASSWORD = config('EMAIL_PASSWORD')   # Your email password


# Default "from" address for outgoing emails
DEFAULT_FROM_EMAIL = config('EMAIL')

# List of email addresses that will receive error messages from Django's logging framework
ADMINS = [
    ('Afaan', config('EMAIL_ADMIN')),
    # Add more tuples as needed
    # 
 ]
# Email subject prefix for error messages sent to admins
EMAIL_SUBJECT_PREFIX = 'IDEAS DAO BACKEND'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = "/media/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Permissions
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ],
}



CKEDITOR_UPLOAD_PATH = "media/"

# SIMPLE_JWT = {
#     "ROTATE_REFRESH_TOKENS": True,
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
# }
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME': timedelta(days=30),
    'SLIDING_TOKEN_REFRESH_LIFETIME_LATE_DELTA': timedelta(days=1),
    'SLIDING_TOKEN_LIFETIME_LATE_DELTA': timedelta(days=30),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_CLAIM': 'user_id',
    'AUTHENTICATION_CLASSES': ('ideasApi.authentication.MemberJWTAuthentication',),
}




# settings.py
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default backend for admin
    # 'user_app.backends.MemberModelBackend'
]

#Logging configuration
# Define the base directory for logs
LOGGING_DIR = os.path.join(BASE_DIR, 'logs')

# Ensure the logs directory exists
os.makedirs(LOGGING_DIR, exist_ok=True)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message} ',
            'style': '{',
        },
    },
    'filters': {
        'exclude_autoreload': {
            '()': 'ideasApi.log_filters.ExcludeAutoreloadFilter',  # Adjust the module path
        },
    },
    'handlers': {
        'proxy_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'proxy.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'user_register_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'userRegister.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'error_file': {
            'level': 'ERROR',  # Capture ERROR level and higher
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'error.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'verbose',
        },
        # 'email_admin': {
        #     'level': 'ERROR',  # Capture ERROR level and higher
        #     'class': 'django.utils.log.AdminEmailHandler',
        #     'formatter': 'verbose',
        # },
        'minimal_email': {
            'level': 'ERROR',  # Capture ERROR level and higher
            'class': 'ideasApi.log_handlers.MinimalEmailHandler',  # Replace with the actual path to your handler
            'formatter': 'verbose',
        },
        'warning_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'warning.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'verbose',
        },
        'regular_file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOGGING_DIR, 'regular.log'),
            'when': 'midnight',
            'backupCount': 7,
            'formatter': 'verbose',
            'filters': ['exclude_autoreload'], 
        },
    },
    'loggers': {
        'proxy_logger': {
            'handlers': ['proxy_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django': {
            'handlers': ['error_file', 'minimal_email', 'warning_file', 'regular_file'],
            'level': 'DEBUG',  # Capture DEBUG level and higher
            'propagate': True,
        },
        'ideasApi.views': {
            'handlers': ['error_file', 'minimal_email', 'warning_file', 'regular_file'],
            'level': 'DEBUG',  # Adjust the level as needed
            'propagate': False,
        },
        'user_app.views': {
            'handlers': ['error_file', 'minimal_email', 'warning_file', 'regular_file','user_register_file'],
            'level': 'DEBUG',  # Adjust the level as needed
            'propagate': False,
        },
    },
}


