from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from davisinteractive.dataset import Davis
from davisinteractive.evaluation import EvaluationService
from davisinteractive.third_party import mask_api

from .decorators import json_response

# Create your views here.
SERVICE = EvaluationService(
    'test-dev',
    davis_root='/Users/alberto/Workspace/CVL/datasets/davis-2017/data/DAVIS',
    max_t=3600,
    max_i=10)


@json_response
@require_GET
def get_dataset_samples(_):
    response = SERVICE.get_samples()

    return response


@json_response
@require_GET
def get_scibble(_, sequence, scribble_idx):
    response = SERVICE.get_scribble(sequence, scribble_idx)
    return response


@csrf_exempt
@json_response
@require_POST
def post_predicted_masks(request):
    user_key = request.META.get('HTTP_USER_KEY')
    session_key = request.META.get('HTTP_SESSION_KEY')
    params = request.json
    params['pred_masks'] = mask_api.decode_batch_masks(params['pred_masks'])
    params['user_key'] = user_key
    params['session_key'] = session_key

    response = SERVICE.post_predicted_masks(**params)
    return response


@json_response
@require_GET
def get_report(request):
    """ Return the report for a single session.
    """
    session_key = request.META.get('HTTP_SESSION_KEY')
    df = SERVICE.get_report(session_id=session_key).copy()
    df = df.groupby(
        ['session_id', 'sequence', 'scribble_idx', 'interaction',
         'object_id']).mean()
    df = df.reset_index()
    return df.to_dict()
