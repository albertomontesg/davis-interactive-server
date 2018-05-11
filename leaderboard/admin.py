from django.contrib import admin

from .models import LeaderboardCurve


# Register your models here.
@admin.register(LeaderboardCurve)
class LeaderboardCurveAdmin(admin.ModelAdmin):
    fields = ('session', 'time', 'jaccard')
    list_display = ('session', 'time', 'jaccard')
    readonly_fields = ('session', 'time', 'jaccard')
