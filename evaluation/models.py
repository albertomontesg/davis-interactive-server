from django.db import models
from django.utils import timezone

from registration.models import Participant


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
        if self.num_entries == service.num_entries:
            self.completed = True
        self.save()


class ResultEntry(models.Model):
    session = models.ForeignKey(Session, on_delete=models.PROTECT, null=False)
    # Entry params
    sequence = models.CharField(max_length=128, blank=False)
    scribble_idx = models.IntegerField()
    interaction = models.IntegerField()
    object_id = models.IntegerField()
    frame = models.IntegerField()
    jaccard = models.FloatField()
    timing = models.FloatField()
