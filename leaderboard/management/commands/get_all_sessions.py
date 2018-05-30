import json

from django.core.management.base import BaseCommand

from evaluation.models import Session


class Command(BaseCommand):  # pragme: no cover
    help = 'Get all finished sessions summary'

    def handle(self, *args, **options):
        sessions = Session.objects.filter(completed=True)
        sessions_data = [
            s.get_summary(shorter_session_id=True) for s in sessions
        ]

        sessions_str = json.dumps({'sessions': sessions_data})

        self.stdout.write(sessions_str)
