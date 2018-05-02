import os

from server.settings.base import *  # pylint: disable=unused-wildcard-import, wildcard-import

DEBUG = False

SECRET_KEY = os.environ.get('SECRET_KEY')

# Evaluation Settings
EVALUATION_SUBSET = os.environ.get('SUBSET')
EVALUATION_DAVIS_ROOT = os.environ.get('DAVIS_ROOT')
EVALUATION_MAX_TIME = os.environ.get('MAX_TIME')
EVALUATION_MAX_INTERACTIONS = os.environ.get('MAX_INTERACTIONS')

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
