import pandas as pd
from django.db.models import Max, QuerySet
from django.shortcuts import render
from django.views.decorators.http import require_GET

from evaluation.decorators import json_api
from evaluation.models import Participant, Session


# @json_api
@require_GET
def get_leaderboard(request):
    leaderboard = {'by_auc': [], 'by_jaccard_threshold': []}

    query = Session.objects.filter(completed=True).values(
        'participant__user_id', 'session_id', 'auc')
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

    query = Session.objects.filter(completed=True).values(
        'participant__user_id', 'session_id', 'jaccard_at_threshold')
    df = pd.DataFrame.from_records(query).set_index('session_id')
    session_ids = df.groupby(
        'participant__user_id').idxmax().values.ravel().tolist()
    sessions = Session.objects.filter(
        session_id__in=session_ids).order_by('-jaccard_at_threshold')
    for i, s in enumerate(sessions):
        pos = i + 1
        summary = s.get_summary(shorter_session_id=True)
        summary['pos'] = pos
        leaderboard['by_jaccard_threshold'].append(summary)

    return render(
        request, 'leaderboard.html', leaderboard)
