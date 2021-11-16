"""
Django settings for era project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

from . import credentials

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = credentials.BASE_DIR


# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = credentials.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = credentials.DEBUG

ALLOWED_HOSTS = credentials.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    "qcm.apps.QcmConfig",
    "qcm.apps.QcmAdminConfig",  # replaces 'django.contrib.admin'
    "polymorphic",
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = credentials.ROOT_URLCONF

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = credentials.WSGI_APPLICATION


# Database

DATABASES = credentials.DATABASES

# Password validation

AUTH_PASSWORD_VALIDATORS = credentials.AUTH_PASSWORD_VALIDATORS


# Internationalization

LANGUAGE_CODE = credentials.LANGUAGE_CODE

TIME_ZONE = credentials.TIME_ZONE

USE_I18N = credentials.USE_I18N

USE_L10N = credentials.USE_L10N

USE_TZ = credentials.USE_TZ


# Static files (CSS, JavaScript, Images)

STATIC_URL = credentials.STATIC_URL
STATIC_ROOT = credentials.STATIC_ROOT

# Default primary key field type

DEFAULT_AUTO_FIELD = credentials.DEFAULT_AUTO_FIELD
