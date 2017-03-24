from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from model_utils.models import TimeStampedModel
from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


@python_2_unicode_compatible
class UserLetter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    letter = models.CharField(max_length=1)

    def __str__(self):
        return u'({}) {}'.format(self.user.username, self.letter.upper())


@python_2_unicode_compatible
class LetterTransaction(models.Model):
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='borrower')
    letter = models.ForeignKey(UserLetter)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return u'({} -> {}) {}'.format(self.letter.user.username, self.borrower.username, self.letter.letter.upper())


@python_2_unicode_compatible
class TeamWord(TimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    word = models.CharField(max_length=30)

    def __str__(self):
        return u'({}) {}'.format(self.user.username, self.word)


@python_2_unicode_compatible
class Dictionary(models.Model):
    word = models.CharField(max_length=100, db_index=True, unique=True)

    def __str__(self):
        return self.word



class Constants(BaseConstants):
    name_in_url = 'anagrams'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass
