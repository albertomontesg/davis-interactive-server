import logging

from django.db import models
from django.utils import timezone

from leaderboard.models import LeaderboardCurve
from registration.models import Participant

logger = logging.getLogger(__name__)


class Session(models.Model):
    session_id = models.CharField(max_length=128, unique=True, primary_key=True)
    participant = models.ForeignKey(
        'registration.Participant', on_delete=models.PROTECT, null=False)
    start_timestamp = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    num_entries = models.IntegerField(default=0)

    # Parameters to evaluate
    auc = models.FloatField(null=True, blank=True)
    time_threshold = models.FloatField(null=True, blank=True)
    jaccard_at_threshold = models.FloatField(null=True, blank=True)

    @staticmethod
    def get_or_create_session(user_id, session_id):
        session = Session.objects.filter(session_id=session_id).first()
        if session is None:
            participant = Participant.objects.filter(user_id=user_id).first()
            if participant is None:
                raise ValueError('user_id do not exists')
            session = Session(session_id=session_id, participant=participant)
            session.save()
        return session

    def __str__(self):
        return f'{self.participant}@{self.session_id[:8]}'

    def update_entries(self, nb_new_entries):
        """ Add the new number of entries to the session.
        """
        self.num_entries += nb_new_entries
        self.save()

    def mark_completed(self, summary):
        """ Mark session completed computing the time vs jaccard curve and
        storing it.
        """
        self.auc = summary['auc']
        self.time_threshold = summary['jaccard_at_threshold']['threshold']
        self.jaccard_at_threshold = summary['jaccard_at_threshold']['jaccard']

        # Add curve to LeaderboardCurve
        entries = [
            LeaderboardCurve(session=self, time=t, jaccard=j) for t, j in zip(
                summary['curve']['time'], summary['curve']['jaccard'])
        ]
        LeaderboardCurve.objects.bulk_create(entries)

        self.completed = True
        self.save()

    def get_summary(self, shorter_session_id=False):
        """ Retrieve the global summary for each the session.
        """
        session_id = self.session_id
        if shorter_session_id:
            session_id = session_id[:8]
        summary = {
            'participant': str(self.participant),
            'session_id': session_id,
            'auc': self.auc,
            'jaccard_at_threshold': {
                'jaccard': self.jaccard_at_threshold,
                'threshold': self.time_threshold
            },
            'curve': {
                'time': [],
                'jaccard': []
            }
        }
        curve = LeaderboardCurve.objects.filter(
            session=self).order_by('time').values('time', 'jaccard')
        for c in curve:
            summary['curve']['time'].append(c['time'])
            summary['curve']['jaccard'].append(c['jaccard'])

        return summary


class ResultEntry(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT, null=False)
    timestamp = models.DateTimeField(default=timezone.now)
    # Entry params
    sequence = models.CharField(max_length=128, blank=False)
    scribble_idx = models.IntegerField()
    interaction = models.IntegerField()
    object_id = models.IntegerField()
    frame = models.IntegerField()
    jaccard = models.FloatField()
    timing = models.FloatField()


class AnnotatedFrame(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT, null=False)
    sequence = models.CharField(max_length=128, blank=False)
    scribble_idx = models.IntegerField()
    frame = models.IntegerField()
    override = models.BooleanField(default=False)
