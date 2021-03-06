"""
Django settings for communityfund project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'd4kvkm2db7me0l',
        'HOST': 'ec2-54-163-226-9.compute-1.amazonaws.com',
        'USER': 'nrnqlyareboewm',
        'PASSWORD': '-sF1PLqn93MbMPR7hDYxXyhygt',
        'PORT': '5432',
    }
}
#import dj_database_url
#DATABASES = {'default': dj_database_url.config(default=os.getenv('HEROKU_POSTGRESQL_ONYX'))}
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ')v7ly^(#*l1t!ob0h7goi*rr5gut-1vui#5q*p(6%b)kwmy9(w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True 

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = (
    BASE_DIR + "/../home/templates/home",
    BASE_DIR + "/home/templates/home",
    )

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'debug_toolbar',
    'floppyforms',
    'crispy_forms',
    'registration',
    'home',
    'fm',
    'multiselectfield'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth', 
    'django.core.context_processors.debug', 
    'django.core.context_processors.i18n', 
    'django.core.context_processors.media', 
    'django.core.context_processors.static', 
    'django.core.context_processors.tz', 
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
)

ROOT_URLCONF = 'communityfund.urls'

WSGI_APPLICATION = 'communityfund.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# uncomment below 6 lines when developing locally
#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2',
#        'NAME': 'communityfund_db',
#    }
#}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, '../static'),
    os.path.join(BASE_DIR, 'static'),
)
'''
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
'''

LOGIN_REDIRECT_URL = '/'
CRISPY_TEMPLATE_PACK = 'bootstrap'

AUTH_PROFILE_MODULE = 'communityfund.UserProfile'
