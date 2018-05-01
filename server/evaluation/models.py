from django.db import models
from django.utils import timezone

from registration.models import Participant


class Session(models.Model):
    session_id = models.CharField(max_length=128, unique=True, primary_key=True)
    participant = models.ForeignKey(
        'registration.Participant', on_delete=models.PROTECT, null=False)
    start_timestamp = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

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
