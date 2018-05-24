import tempfile
from datetime import datetime

import pytz

from server.settings.base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd9ns*-47^jva++xnop-$+sn&p!!7g4h8-s!a3+7b0-j)c!as*h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Evaluation Settings
EVALUATION_SUBSET = 'test-dev'
EVALUATION_DAVIS_ROOT = os.path.join(tempfile.mkdtemp(), 'DAVIS')
EVALUATION_MAX_TIME = 3600
EVALUATION_MAX_INTERACTIONS = 10
EVALUATION_TIME_THRESHOLD = 60
EVALUATION_DEADLINE = datetime.strptime(
    os.environ.get('DEADLINE', '25 May 2018 23:59'), '%d %b %Y %H:%M')
EVALUATION_DEADLINE = pytz.utc.localize(EVALUATION_DEADLINE)

# Disable logging
LOGGING = None
