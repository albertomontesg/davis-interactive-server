from django.contrib import admin

from .models import LeaderboardCurve


# Register your models here.
@admin.register(LeaderboardCurve)
class LeaderboardCurveAdmin(admin.ModelAdmin):
    fields = ('session', 'time', 'metric')
    list_display = ('session', 'time', 'metric')
    readonly_fields = ('session', 'time', 'metric')
