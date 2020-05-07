from davisinteractive import logging
from davisinteractive.evaluation import EvaluationService as _EvaluationService
from django.conf import settings

from .storage import DBStorage

logging.set_info_level(2)

_ROBOT_DEFAULT_PARAMETERS = {
    'kernel_size': .1,
    'max_kernel_radius': 16,
    'min_nb_nodes': 2,
    'nb_points': 1000,
}


class EvaluationService(object):
    """ Singleton wrapper over EvaluationService class"""
    instance = None

    def __new__(cls):
        if not EvaluationService.instance:
            EvaluationService.instance = _EvaluationService(
                settings.EVALUATION_SUBSET,
                storage=DBStorage,
                robot_parameters=_ROBOT_DEFAULT_PARAMETERS,
                davis_root=settings.EVALUATION_DAVIS_ROOT,
                max_t=settings.EVALUATION_MAX_TIME,
                max_i=settings.EVALUATION_MAX_INTERACTIONS,
                metric_to_optimize=settings.EVALUATION_METRIC_TO_OPTIMIZE,
                time_threshold=settings.EVALUATION_TIME_THRESHOLD)
        return EvaluationService.instance

    def __getattr__(self, name):  # pragma: no cover
        return getattr(self.instance, name)

    def __setattr__(self, name, value):  # pragma: no cover
        return setattr(self.instance, name, value)
