import os

from server.settings.base import *  # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# Evaluation Settings
EVALUATION_SUBSET = os.environ.get('SUBSET')
EVALUATION_DAVIS_ROOT = os.environ.get('DAVIS_ROOT')
EVALUATION_MAX_TIME = int(os.environ.get('MAX_TIME'))
EVALUATION_MAX_INTERACTIONS = int(os.environ.get('MAX_INTERACTIONS'))
EVALUATION_TIME_THRESHOLD = int(os.environ.get('TIME_THRESHOLD'))
assert EVALUATION_MAX_INTERACTIONS is not None

# Email configurations
EMAIL_SILENT = False
EMAIL_SECRETS_DIR = os.environ.get('EMAIL_SECRETS_DIR')
EMAIL_CLIENT_SECRET_FILE = 'client_secret.json'
EMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.send'
EMAIL_APPLICATION_NAME = 'Gmail API Python Send Email'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '5432',
        'CONN_MAX_AGE': 120,
    }
}

ALLOWED_HOSTS = ['*']
STATIC_URL = 'https://storage.googleapis.com/davis-interactive-static/static/'
