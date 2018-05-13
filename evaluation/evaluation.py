from django.conf import settings

from davisinteractive import logging
from davisinteractive.evaluation import EvaluationService as _EvaluationService

from .storage import DBStorage

logging.set_info_level(2)


class EvaluationService(object):
    """ Singleton wrapper over EvaluationService class"""
    instance = None

    def __new__(cls):
        if not EvaluationService.instance:
            EvaluationService.instance = _EvaluationService(
                settings.EVALUATION_SUBSET,
                storage=DBStorage,
                davis_root=settings.EVALUATION_DAVIS_ROOT,
                max_t=settings.EVALUATION_MAX_TIME,
                max_i=settings.EVALUATION_MAX_INTERACTIONS,
                time_threshold=settings.EVALUATION_TIME_THRESHOLD)
        return EvaluationService.instance

    def __getattr__(self, name):  # pragma: no cover
        return getattr(self.instance, name)

    def __setattr__(self, name, value):  # pragma: no cover
        return setattr(self.instance, name, value)
