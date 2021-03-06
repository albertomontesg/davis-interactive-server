import os
from datetime import datetime

import pytz

from server.settings.base import *  # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# Evaluation Settings
EVALUATION_SUBSET = os.environ.get('SUBSET')
EVALUATION_DAVIS_ROOT = os.environ.get('DAVIS_ROOT')
EVALUATION_MAX_TIME = int(os.environ.get('MAX_TIME'))
EVALUATION_MAX_INTERACTIONS = int(os.environ.get('MAX_INTERACTIONS'))
EVALUATION_TIME_THRESHOLD = int(os.environ.get('TIME_THRESHOLD'))
EVALUATION_METRIC_TO_OPTIMIZE = os.environ.get('METRIC_TO_OPTIMIZE')
EVALUATION_DEADLINE = datetime.strptime(
    os.environ.get('DEADLINE'), '%d %b %Y %H:%M')
EVALUATION_DEADLINE = pytz.utc.localize(EVALUATION_DEADLINE)
assert EVALUATION_MAX_INTERACTIONS is not None

# Email configurations
EMAIL_SILENT = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': os.getenv('DATABASE_PORT'),
        'CONN_MAX_AGE': 120,
    }
}

ALLOWED_HOSTS = ['*']
STATIC_URL = 'https://storage.googleapis.com/davis-interactive-static/static/'
