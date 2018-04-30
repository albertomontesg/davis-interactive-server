from django.db import models
from django.utils import timezone


class Session(models.Model):
    session_id = models.CharField(max_length=128, unique=True)
    user_id = models.CharField(max_length=128)
    start_timestamp = models.DateTimeField(default=timezone.now)
    completed = models.BooleanField(default=False)

    @staticmethod
    def get_or_create_session(user_id, session_id):
        session = Session.objects.filter(session_id=session_id).first()
        if session is None:
            session = Session(session_id=session_id, user_id=user_id)
            session.save()
        return session

    def __str__(self):
        return f'{self.user_id}@{self.session_id[:8]}'


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
