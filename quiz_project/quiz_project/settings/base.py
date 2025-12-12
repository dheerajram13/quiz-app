"""
Base settings for quiz_project.
This file contains common settings shared across all environments.
"""

import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',

    # Local apps
    'quiz_api',
]


# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
    ],
    'EXCEPTION_HANDLER': 'quiz_api.exceptions.custom_exception_handler',
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',  # 100 requests per hour for anonymous users
        'user': '1000/hour',  # 1000 requests per hour for authenticated users
        'login': '10/hour',  # Custom throttle for login attempts
    },
}


# API Documentation Configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'Quiz Application API',
    'DESCRIPTION': """
    A comprehensive RESTful API for a quiz application.

    ## Features
    - User authentication with JWT tokens
    - Quiz management and retrieval
    - Multiple question types (single, multiple, select-words)
    - Automatic scoring and grading
    - User statistics and performance tracking

    ## Authentication
    Most endpoints require authentication. Use the `/api/token/` endpoint to obtain JWT tokens.
    Include the access token in the Authorization header: `Authorization: Bearer <token>`
    """,
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'CONTACT': {
        'name': 'API Support',
        'email': 'support@quizapp.com',
    },
    'LICENSE': {
        'name': 'MIT License',
    },
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/',
}


MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


ROOT_URLCONF = 'quiz_project.urls'

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

WSGI_APPLICATION = 'quiz_project.wsgi.application'


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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'


# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Create logs directory if it doesn't exist
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)


# Database Routers Configuration
# Uncomment and configure based on your multi-database needs
# See quiz_project/db_routers.py for available router classes and documentation

# DATABASE_ROUTERS = []

# Example configurations (uncomment and customize as needed):

# 1. Read/Write Splitting (Primary-Replica setup)
# DATABASE_ROUTERS = ['quiz_project.db_routers.PrimaryReplicaRouter']

# 2. App-based routing (Different apps use different databases)
# DATABASE_ROUTERS = ['quiz_project.db_routers.AppBasedRouter']
# APP_DB_ROUTING = {
#     'quiz_api': 'default',
#     'analytics': 'analytics_db',
# }

# 3. Model-based routing (Fine-grained control per model)
# DATABASE_ROUTERS = ['quiz_project.db_routers.ModelBasedRouter']
# MODEL_DB_ROUTING = {
#     'quiz_api.UserActivity': 'analytics_db',
#     'quiz_api.AuditLog': 'logging_db',
#     '_default': 'default',
# }

# 4. Hybrid routing (App-based + Read/Write splitting)
# DATABASE_ROUTERS = ['quiz_project.db_routers.HybridRouter']
# HYBRID_DB_ROUTING = {
#     'quiz_api': {'primary': 'default', 'replica': 'default_replica'},
#     'analytics': {'primary': 'analytics_db', 'replica': 'analytics_replica'},
# }

# 5. Multiple routers (evaluated in order)
# DATABASE_ROUTERS = [
#     'quiz_project.db_routers.ModelBasedRouter',
#     'quiz_project.db_routers.PrimaryReplicaRouter',
# ]
