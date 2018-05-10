import logging

from django.db import models
from django.utils import timezone

from registration.models import Participant

logger = logging.getLogger(__name__)


class Session(models.Model):
    session_id = models.CharField(max_length=128, unique=True, primary_key=True)
    participant = models.ForeignKey(
        'registration.Participant', on_delete=models.PROTECT, null=False)
    start_timestamp = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)
    num_entries = models.IntegerField(default=0)

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

        This will mark as completed the session when reached the total number
        of entries of the EvaluationService.
        """
        from .evaluation import EvaluationService
        service = EvaluationService()
        self.num_entries += nb_new_entries
        # Completion is defined as there is at least one interaction for each
        # sample
        samples_in_session = ResultEntry.objects.filter(
            session=self, interaction=1, object_id=1, frame=0).values(
                'sequence', 'scribble_idx')
        samples_in_session = [
            (s['sequence'], s['scribble_idx']) for s in samples_in_session
        ]
        samples, _, _ = service.get_samples()
        if not self.completed and set(samples) == set(samples_in_session):
            logger.info(f'Session {self} completed')
            self.completed = True
        self.save()


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
