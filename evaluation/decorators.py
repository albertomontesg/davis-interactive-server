import json
from functools import wraps

from django.http import HttpResponse, JsonResponse

from .evaluation import EvaluationService


def json_response(func):

    def decorator(request, *args, **kwargs):
        if request.content_type == 'application/json':
            if request.body:
                request.json = json.loads(request.body)
            else:
                request.json = None

        objects = func(request, *args, **kwargs)

        if isinstance(objects, HttpResponse):
            return objects
        return JsonResponse(objects, safe=False)

    return decorator


def require_service(func):

    def decorator(*args, **kwargs):
        service = EvaluationService()
        kwargs['service'] = service
        response = func(*args, **kwargs)
        return response

    return decorator
