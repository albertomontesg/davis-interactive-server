import pandas as pd
from django.conf import settings
from django.db.models import Max, QuerySet
from django.http import JsonResponse
from django.shortcuts import render
from django.utils import timezone
from django.views.decorators.clickjacking import xframe_options_exempt
from django.views.decorators.http import require_GET

from evaluation.decorators import json_api
from evaluation.models import Participant, Session


@xframe_options_exempt
@require_GET
def get_leaderboard(request):
    leaderboard = {'by_auc': [], 'by_metric_threshold': []}

    deadline = settings.EVALUATION_DEADLINE

    query = Session.objects.filter(
        completed=True,
        show_at_leaderboard=True, start_timestamp__lte=deadline).values(
            'participant__user_id', 'session_id', 'auc')
    if len(query) == 0 and request.content_type == 'application/json':
        return JsonResponse(leaderboard)
    elif len(query) == 0:
        return render(request, 'leaderboard.html', leaderboard)

    df = pd.DataFrame.from_records(query).set_index('session_id')
    session_ids = df.groupby(
        'participant__user_id').idxmax().values.ravel().tolist()
    sessions = Session.objects.filter(
        session_id__in=session_ids).order_by('-auc')
    for i, s in enumerate(sessions):
        pos = i + 1
        summary = s.get_summary(shorter_session_id=True)
        summary['pos'] = pos
        leaderboard['by_auc'].append(summary)

    query = Session.objects.filter(
        completed=True,
        show_at_leaderboard=True, start_timestamp__lte=deadline).values(
            'participant__user_id', 'session_id', 'metric_at_threshold')
    df = pd.DataFrame.from_records(query).set_index('session_id')
    session_ids = df.groupby(
        'participant__user_id').idxmax().values.ravel().tolist()
    sessions = Session.objects.filter(
        session_id__in=session_ids).order_by('-metric_at_threshold')
    for i, s in enumerate(sessions):
        pos = i + 1
        summary = s.get_summary(shorter_session_id=True)
        summary['pos'] = pos
        leaderboard['by_metric_threshold'].append(summary)

    if request.content_type == 'application/json':
        return JsonResponse(leaderboard)
    response = render(request, 'leaderboard.html', leaderboard)
    response['Expose-Height-Cross-Origin'] = 1
    return response
