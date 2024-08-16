"""
Django settings for solicitudesfua project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-2gz6)+&hrycppniy*qre!h$!o!7r7g96oee6(ui2hso5f=3e@8'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

WSGI_APPLICATION = 'solicitudesfua.wsgi.application'

USE_TZ = False

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
#DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = ['*']
# Lista de IDs de grupos permitidos
ALLOWED_GROUPS = [
    "425ddb39-836e-47d6-98cd-0a4015d1563e",
]
# azure ad settings
AZURE_AUTH = {
    "CLIENT_ID": os.getenv('CLIENT_ID'),
    "CLIENT_SECRET": os.getenv('CLIENT_SECRET'),
    "REDIRECT_URI": os.getenv('REDIRECT_URI'),
    "SCOPES": ["User.Read", "GroupMember.Read.All", "Directory.Read.All", "User.Read.All"],
    "AUTHORITY": os.getenv('AUTHORITY'),
    "LOGOUT_URI": os.getenv('LOGOUT_URI'),
    "PUBLIC_URLS": ['index'],  # Optional, public views accessible by non-authenticated users
    "PUBLIC_PATHS": ['/',],  # Optional, public paths accessible by non-authenticated users
    "ROLES": {
        "425ddb39-836e-47d6-98cd-0a4015d1563e": "Gestion Tecnologica e innovacion"
    }  # Optional, will add user to django group if user is in EntraID group
}

LOGIN_URL = "/azure_auth/login"
LOGIN_REDIRECT_URL = "home/"    # Or any other endpoint

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'softwareids',
    "azure_auth",
]

AUTHENTICATION_BACKENDS = ("azure_auth.backends.AzureBackend",)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'softwareids.middleware.EnsureAccessTokenMiddleware',  # Colocado después de SessionMiddleware
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # "azure_auth.middleware.AzureMiddleware",
]


ROOT_URLCONF = 'solicitudesfua.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,'templates'),
        ],
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

WSGI_APPLICATION = 'solicitudesfua.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '5432',
    }
}

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



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
# Configuraciones de seguridad para producción
SECURE_SSL_REDIRECT = True  # Redirige todas las solicitudes HTTP a HTTPS

# Asegura las cookies
SESSION_COOKIE_SECURE = True  # Solo enviar cookies de sesión a través de HTTPS
CSRF_COOKIE_SECURE = True     # Solo enviar la cookie CSRF a través de HTTPS
SECURE_HSTS_SECONDS = 31536000  # Configura HSTS para forzar HTTPS
SECURE_HSTS_INCLUDE_SUBDOMAINS = True  # Aplica HSTS a todos los subdominios
SECURE_HSTS_PRELOAD = True  # Permite que los navegadores incluyan tu sitio en la lista de precarga de HSTS
SECURE_REFERRER_POLICY = 'strict-origin'  # Limita la información que se envía en el encabezado Referer

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'templates/static/')
]
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
