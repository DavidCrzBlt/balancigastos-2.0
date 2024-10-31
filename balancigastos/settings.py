"""
Django settings for balancigastos project.

Generated by 'django-admin startproject' using Django 5.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""


import os
import sys

from pathlib import Path
import dj_database_url
from django.core.management.utils import get_random_secret_key

from dotenv import load_dotenv

from django.contrib.messages import constants as message_constants


# Carga el archivo .env según el entorno
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')
if ENVIRONMENT == 'production':
    load_dotenv('.env.production')
else:
    load_dotenv('.env.local')


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('DJANGO_SECRET_KEY',get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG','False') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS','127.0.0.1,localhost').split(',')

# Application definition

SHARED_APPS = (
    'django_tenants',  # mandatory
    'clientes', # you must list the app where your tenant model resides in

    'django.contrib.contenttypes',

    # everything below here is optional
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

TENANT_APPS = (
    # your tenant-specific apps
    'proyectos.apps.ProyectosConfig',
    'contabilidad.apps.ContabilidadConfig',
    'equipos_y_vehiculos.apps.EquiposYVehiculosConfig',
    'usuarios.apps.UsuariosConfig',
    'empleados.apps.EmpleadosConfig',
)

INSTALLED_APPS = SHARED_APPS + TENANT_APPS

TENANT_MODEL = "clientes.Cliente" 

TENANT_DOMAIN_MODEL = "clientes.DominioCliente"  

MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'balancigastos.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR,'templates/')

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'balancigastos.utils.context_processors.get_profile_username',
            ],
        },
    },
]

WSGI_APPLICATION = 'balancigastos.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DEVELOPMENT_MODE = os.getenv('DEVELOPMENT_MODE','False') == 'True'

# Configuración de base de datos

DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}
DATABASES["default"]["ENGINE"] = "django_tenants.postgresql_backend"

DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

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

TIME_ZONE = 'America/Mexico_City'

USE_I18N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# Ruta estática
STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    ]

# Si estás en producción
if ENVIRONMENT == 'production':
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'proyectos:proyectos'

LOGOUT_REDIRECT_URL = 'usuarios:login'

MESSAGE_TAGS = {
    message_constants.DEBUG: 'secondary',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger',
}
