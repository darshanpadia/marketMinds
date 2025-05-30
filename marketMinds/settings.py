"""
Django settings for marketMinds project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/


if os.getenv("ENV", "development") != "production":
    load_dotenv(BASE_DIR / ".env")
    
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", "False") == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")

AUTH_USER_MODEL = 'users.CustomUser'
# CELERY_BROKER_URL = 'django://'
# CELERY_RESULT_BACKEND = 'django-db'

# # run tasks at specific intervals
# CELERY_BEAT_SCHEDULE = {
    
# }

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '5/min',
    },
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    'users',
    'dashboard',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    
]

ROOT_URLCONF = 'marketMinds.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'marketMinds.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

datase_url = os.environ.get("DATABASE_URL")
DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default=datase_url,
        conn_max_age=600
    )
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

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUDINARY_URL' : os.environ.get('CLOUDINARY_URL')
}

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = "home"  #specify where to redirect the user upon a successful login.
LOGOUT_REDIRECT_URL = "home" #specify where to redirect the user upon a successful logout.

# settings.py

...

if not DEBUG:
    # Security for production
    CSRF_COOKIE_SECURE = True #Ensures CSRF cookies are sent over https connections
    SESSION_COOKIE_SECURE = True

    # If you're using HTTPS (Render uses HTTPS)
    SECURE_SSL_REDIRECT = True # redirects all http requests to https 
    # SECURE_HSTS_SECONDS = 3600 #Enables hsts for 1 hour
    # SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # SECURE_HSTS_PRELOAD = True

    # Optional but good for extra safety
    SECURE_BROWSER_XSS_FILTER = True # enables the browser's built-in XSS protection(usually in older browsers)
    SECURE_CONTENT_TYPE_NOSNIFF = True # prevents the browser from trying to guess the file type


# CORS Settings (allow Vite dev server only in development)
if DEBUG:
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:5173",
    ]
else:
    FRONTEND_URL = os.environ.get("VITE_API_BASE_URL")  # e.g. "https://your-react-app.onrender.com"

    CORS_ALLOWED_ORIGINS = [
        FRONTEND_URL
    ] if FRONTEND_URL else []

    CSRF_TRUSTED_ORIGINS = [
        FRONTEND_URL
    ] if FRONTEND_URL else []

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s:%(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'celery': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

