import json

from django.core.management.base import BaseCommand
from django.db.models import Count, Q

from registration.models import Participant


class Command(BaseCommand):  # pragme: no cover
    help = 'Get participants_stats'

    def handle(self, *args, **options):
        participants = Participant.objects.values(
            'name', 'organization').annotate(
                sessions_total=Count('session'),
                sessions_completed=Count(
                    'session', filter=Q(session__completed=True)))

        participants = {'participants_stats': list(participants)}
        participants_stats = json.dumps(participants)
        self.stdout.write(participants_stats)
