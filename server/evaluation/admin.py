from django.contrib import admin

from .models import ResultEntry, Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    fields = ('session_id', 'user_id', 'start_timestamp', 'completed')
    list_display = ('user_id', 'hash_session_id', 'start_timestamp',
                    'completed')
    list_filter = ('user_id', 'start_timestamp', 'completed')
    readonly_fields = ('session_id', 'user_id', 'start_timestamp')
    actions = []

    def hash_session_id(self, obj):
        return obj.session_id[:8]


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
