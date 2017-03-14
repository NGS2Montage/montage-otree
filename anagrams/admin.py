from django.contrib import admin

from reversion.admin import VersionAdmin

from .models import UserLetter, LetterTransaction, TeamWord


@admin.register(TeamWord)
class TeamWordAdmin(VersionAdmin):
    list_display = ('word', 'user')


@admin.register(LetterTransaction)
class LetterTransactionAdmin(VersionAdmin):
    pass


@admin.register(UserLetter)
class UserLetterAdmin(VersionAdmin):
    list_display = ('letter', 'user', 'pk')
