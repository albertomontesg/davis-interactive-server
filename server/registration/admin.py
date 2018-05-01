from django.contrib import admin

from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    fields = ('user_id', 'name', 'organization', 'email',
              'registration_datetime')
    list_display = ('user_id', 'name', 'organization', 'email',
                    'registration_datetime')
    list_filter = ('organization', 'registration_datetime')
