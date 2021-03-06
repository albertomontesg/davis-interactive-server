import json
import logging
import time
import traceback
from functools import wraps

from django.http import HttpResponse, JsonResponse

from registration.models import Participant

from .evaluation import EvaluationService

logger = logging.getLogger('views')


def json_api(func):

    def decorator(request, *args, **kwargs):
        if request.content_type == 'application/json':
            if request.body:
                request.json = json.loads(request.body)
            else:
                request.json = None
        try:
            objects = func(request, *args, **kwargs)

            if isinstance(objects, HttpResponse):
                return objects
            return JsonResponse(objects, safe=False)
        except Exception as e:
            logger.error(traceback.format_exc())
            error_body = {
                'error': e.__class__.__name__,
                'message': list(e.args)
            }
            return JsonResponse(error_body, status=400)

    return decorator


def require_service(func):

    def decorator(*args, **kwargs):
        service = EvaluationService()
        kwargs['service'] = service
        response = func(*args, **kwargs)
        return response

    return decorator


def authorize(func):

    def decorator(request, *args, **kwargs):
        user_key = request.META.get('HTTP_USER_KEY')
        session_key = request.META.get('HTTP_SESSION_KEY')
        participant = Participant.objects.filter(user_id=user_key).first()
        if not user_key or not session_key or not participant:
            return JsonResponse({
                'error':
                'Invalid user_key or session_key',
                'message': (f'user_key: {user_key}\tsession_key: '
                            f'{session_key} not valid.')
            },
                                status=401)

        kwargs['user_key'] = user_key
        kwargs['session_key'] = session_key
        t_s = time.time()
        response = func(request, *args, **kwargs)
        t_e = time.time()
        logger.info('[Session {}] {} Request time: {:.3f}s'.format(
            session_key[:8], request.path, t_e - t_s))
        return response

    return decorator
