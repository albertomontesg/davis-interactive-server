from server.settings.base import *  # pylint: disable=unused-wildcard-import, wildcard-import

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'd9ns*-47^jva++xnop-$+sn&p!!7g4h8-s!a3+7b0-j)c!as*h'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Evaluation Settings
EVALUATION_SUBSET = os.environ.get('SUBSET', 'train')
EVALUATION_DAVIS_ROOT = os.environ.get('DAVIS_ROOT')
EVALUATION_MAX_TIME = os.environ.get('MAX_TIME', 3600)
EVALUATION_MAX_INTERACTIONS = os.environ.get('MAX_INTERACTIONS', 10)