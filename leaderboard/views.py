from django.db.models import Max, QuerySet
from django.shortcuts import render
from django.views.decorators.http import require_GET

from evaluation.decorators import json_api
from evaluation.models import Participant, Session


# @json_api
@require_GET
def get_leaderboard(request):
    leaderboard = {'by_auc': [], 'by_jaccard_threshold': []}

    participants = Participant.objects.annotate(max_auc=Max(
        'session__auc')).exclude(max_auc__isnull=True).order_by('-max_auc')
    for i, p in enumerate(participants):
        pos = i + 1
        session = Session.objects.get(participant=p, auc=p.max_auc)
        summary = session.get_summary(shorter_session_id=True)
        summary['pos'] = pos
        leaderboard['by_auc'].append(summary)

    participants = Participant.objects.annotate(
        max_jac_th=Max('session__jaccard_at_threshold')).exclude(
            max_jac_th__isnull=True).order_by('-max_jac_th')
    for i, p in enumerate(participants):
        pos = i + 1
        session = Session.objects.get(
            participant=p, jaccard_at_threshold=p.max_jac_th)
        summary = session.get_summary(shorter_session_id=True)
        summary['pos'] = pos
        leaderboard['by_jaccard_threshold'].append(summary)

    return render(
        request, 'leaderboard.html', {
            'by_auc': leaderboard['by_auc'],
            'by_jaccard_threshold': leaderboard['by_jaccard_threshold']
        })
