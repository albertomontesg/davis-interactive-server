import os

from server.settings.base import *  # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# Evaluation Settings
EVALUATION_SUBSET = os.environ.get('SUBSET')
EVALUATION_DAVIS_ROOT = os.environ.get('DAVIS_ROOT')
EVALUATION_MAX_TIME = int(os.environ.get('MAX_TIME'))
EVALUATION_MAX_INTERACTIONS = int(os.environ.get('MAX_INTERACTIONS'))
assert EVALUATION_MAX_INTERACTIONS is not None

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'davis-interactive-test',
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

ALLOWED_HOSTS = ['*']
STATIC_URL = 'http://storage.googleapis.com/davis-interactive-static/static/'
