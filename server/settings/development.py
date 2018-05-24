import os
from datetime import datetime

import pytz

from server.settings.base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd9ns*-47^jva++xnop-$+sn&p!!7g4h8-s!a3+7b0-j)c!as*h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Evaluation Settings
EVALUATION_SUBSET = os.environ.get('SUBSET', 'test-dev')
EVALUATION_DAVIS_ROOT = os.environ.get('DAVIS_ROOT', 'data/DAVIS')
EVALUATION_MAX_TIME = int(os.environ.get('MAX_TIME', 240))
EVALUATION_MAX_INTERACTIONS = int(os.environ.get('MAX_INTERACTIONS', 8))
EVALUATION_TIME_THRESHOLD = int(os.environ.get('TIME_THRESHOLD', 60))
EVALUATION_DEADLINE = datetime.strptime(
    os.environ.get('DEADLINE', '25 May 2018 23:59'), '%d %b %Y %H:%M')
EVALUATION_DEADLINE = pytz.utc.localize(EVALUATION_DEADLINE)
assert EVALUATION_MAX_INTERACTIONS is not None

# New Email configurations
EMAIL_SILENT = True
EMAIL_SECRETS_DIR = os.path.join(BASE_DIR, '.credentials')
EMAIL_CLIENT_SECRET_FILE = 'client_secret.json'
EMAIL_SCOPE = 'https://www.googleapis.com/auth/gmail.send'
EMAIL_APPLICATION_NAME = 'Gmail API Python Send Email'

ALLOWED_HOSTS = ['*']
STATIC_URL = 'https://storage.googleapis.com/davis-interactive-static/static/'
