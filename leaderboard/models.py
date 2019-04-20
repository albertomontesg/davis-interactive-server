from django.db import models


class LeaderboardCurve(models.Model):
    session = models.ForeignKey(
        'evaluation.Session', on_delete=models.PROTECT, null=False)
    # Parameters to evaluate
    time = models.FloatField()
    metric = models.FloatField()
