from django.contrib import admin
from . import models


@admin.register(models.UserParticipantAssociation)
class UserParticipantAssociationAdmin(admin.ModelAdmin):
    list_display = ('user', 'session', 'session_name', 'participant', 'money_earned', 'consent')

