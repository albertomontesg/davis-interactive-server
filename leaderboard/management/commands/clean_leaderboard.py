from django.core.management.base import BaseCommand, CommandError

from evaluation.models import Session
from leaderboard.models import LeaderboardCurve


class Command(BaseCommand):  # pragme: no cover
    help = 'Clean all the leaderboard before recomputing it'

    def handle(self, *args, **options):
        LeaderboardCurve.objects.all().delete()
        Session.objects.all().update(
            auc=None, time_threshold=None, jaccard_at_threshold=None)
        self.stdout.write(
            self.style.SUCCESS('Successfully deleted all leaderboard entries'))
