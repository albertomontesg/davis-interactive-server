from django.core.management.base import BaseCommand, CommandError

from evaluation.evaluation import EvaluationService
from evaluation.models import Session
from leaderboard.models import LeaderboardCurve


class Command(BaseCommand):  # pragme: no cover
    help = 'Clean all the leaderboard before recomputing it'

    def handle(self, *args, **options):
        sessions = Session.objects.filter(completed=True)
        nb_sessions = len(sessions)

        service = EvaluationService()

        for s in sessions:
            report = service.get_report(session_id=s.session_id).copy()
            summary = service.summarize_report(report)
            s.mark_completed(summary)
            s.save()

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully build the leaderboard for {nb_sessions} entries')
        )
