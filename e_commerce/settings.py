"""
Django settings for e_commerce project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

TEMPLATE_DIR = os.path.join(BASE_DIR , 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-(qul&=yg%6&#ube2mq27adl75%a)^r2)v&(^s5r9-zmjzhg$4z'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [ 'localhost',
    '127.0.0.1',
    'homemade-items-i9cpan588-misbah-yousafs-projects.vercel.app',
    '.vercel.app',  ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'siteApp',
    'account',
    'home',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'e_commerce.breadcrumb_middleware.BreadcrumbMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'e_commerce.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'e_commerce.wsgi.application'


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

TIME_ZONE = 'Asia/Karachi'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'public/static')
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'public/static')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

from dotenv import load_dotenv
import os
load_dotenv()


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_PORT = 587 
EMAIL_USE_TLS = True  
EMAIL_HOST_USER = 'misbahyousaf00@gmail.com'  
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD_KEY')  

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'



# Create your views here.
JAZZCASH_MERCHANT_ID = os.getenv('JAZZCASH_MERCHANT_ID_KEY')
JAZZCASH_PASSWORD = os.getenv("JAZZCASH_PASSWORD_KEY")
JAZZCASH_RETURN_URL = "http://127.0.0.1:8000/success"
JAZZCASH_INTEGRITY_SALT = os.getenv('JAZZCASH_INTEGRITY_SALT_KEY')