""" Server views for evaluation.
"""
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from davisinteractive.third_party import mask_api

from .decorators import authorize, json_api, require_service
from .models import Session


@json_api
@require_GET
def get_health(_):
    """ Return Healt status.
    """
    return {
        'health': 'OK',
        'name': 'DAVIS Interactive Server',
        'magic': 23,
        'evaluation_parameters': {
            'subset': settings.EVALUATION_SUBSET,
            'max_time': settings.EVALUATION_MAX_TIME,
            'max_interactions': settings.EVALUATION_MAX_INTERACTIONS
        }
    }


@json_api
@require_GET
@require_service
def get_dataset_samples(_, service):
    """ Return the dataset samples.
    """
    response = service.get_samples()

    return response


@json_api
@require_GET
@require_service
def get_scribble(_, sequence, scribble_idx, service, **kwargs):
    """ Return the scribble asked.
    """
    response = service.get_scribble(sequence, scribble_idx)
    return response


@csrf_exempt
@json_api
@require_POST
@require_service
@authorize
def post_predicted_masks(request, service, user_key, session_key):
    """ Post the predicted masks and return a new scribble.
    """
    params = request.json
    params['pred_masks'] = mask_api.decode_batch_masks(params['pred_masks'])
    params['user_key'] = user_key
    params['session_key'] = session_key

    response = service.post_predicted_masks(**params)
    return response


@json_api
@require_GET
@require_service
@authorize
def get_report(_, service, session_key, user_key=None):
    """ Return the report for a single session.
    """
    df = service.get_report(session_id=session_key).copy()
    if len(df) > 0:
        df = df.groupby([
            'session_id', 'sequence', 'scribble_idx', 'interaction', 'object_id'
        ]).mean()
        df = df.drop(columns='frame')
        df = df.reset_index()
    return df.to_dict()


@csrf_exempt
@json_api
@require_POST
@require_service
@authorize
def post_finish(_, service, session_key, user_key=None):
    """ Notify the session has finished.

    Will mask the session as completed.
    Returns the generated global summary.
    """
    session = Session.objects.get(session_id=session_key)
    report = service.get_report(session_id=session_key)
    summary = service.summarize_report(report)

    session.mark_completed(summary)
    session.save()
    return summary
