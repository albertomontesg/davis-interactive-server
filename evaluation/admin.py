from django.contrib import admin

from .evaluation import EvaluationService
from .models import ResultEntry, Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    fields = ('session_id', 'participant', 'start_timestamp', 'completed')
    list_display = ('participant', 'hash_session_id', 'start_timestamp',
                    'completed', 'completed_percentage')
    list_filter = ('participant', 'start_timestamp', 'completed')
    readonly_fields = ('session_id', 'participant', 'start_timestamp')
    actions = []

    def hash_session_id(self, obj):  # pragma: no cover
        return obj.session_id[:8]

    def completed_percentage(self, obj):  # pragma: no cover
        fraction = obj.num_entries / EvaluationService().num_entries
        return f'{fraction * 100: .2f}%'


@admin.register(ResultEntry)
class ResultEntryAdmin(admin.ModelAdmin):
    fields = ('session', 'sequence', 'scribble_idx', 'interaction', 'object_id',
              'frame', 'jaccard', 'timing')

    list_display = ('session', 'sequence', 'scribble_idx', 'object_id',
                    'interaction', 'frame', 'jaccard')
    list_filter = ('session', 'session__start_timestamp', 'session__completed',
                   'sequence')
    readonly_fields = ('session', 'sequence', 'scribble_idx', 'interaction',
                       'object_id', 'frame', 'jaccard', 'timing')
