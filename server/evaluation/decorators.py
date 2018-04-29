import json

from django.http import HttpResponse, JsonResponse


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
