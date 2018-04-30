""" Server views for evaluation.
"""
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from davisinteractive.third_party import mask_api

from .decorators import json_response, require_service


@json_response
@require_GET
def get_health(_):
    """ Return Healt status.
    """
    return {'health': 'OK', 'name': 'DAVIS Interactive Server', 'magic': 23}


@json_response
@require_GET
@require_service
def get_dataset_samples(_, service):
    """ Return the dataset samples.
    """
    response = service.get_samples()

    return response


@json_response
@require_GET
@require_service
def get_scribble(_, sequence, scribble_idx, service, **kwargs):
    """ Return the scribble asked.
    """
    response = service.get_scribble(sequence, scribble_idx)
    return response


@csrf_exempt
@json_response
@require_POST
@require_service
def post_predicted_masks(request, service):
    """ Post the predicted masks and return a new scribble.
    """
    user_key = request.META.get('HTTP_USER_KEY')
    session_key = request.META.get('HTTP_SESSION_KEY')
    params = request.json
    params['pred_masks'] = mask_api.decode_batch_masks(params['pred_masks'])
    params['user_key'] = user_key
    params['session_key'] = session_key

    response = service.post_predicted_masks(**params)
    return response


@json_response
@require_GET
@require_service
def get_report(request, service):
    """ Return the report for a single session.
    """
    session_key = request.META.get('HTTP_SESSION_KEY')
    df = service.get_report(session_id=session_key).copy()
    if len(df) > 0:
        df = df.groupby([
            'session_id', 'sequence', 'scribble_idx', 'interaction', 'object_id'
        ]).mean()
        df = df.reset_index()
    return df.to_dict()
