import tempfile

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
