from django.contrib import admin

from .models import Result, Session


@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    pass


@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    pass
