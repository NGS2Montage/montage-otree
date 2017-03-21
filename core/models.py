from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from otree.models import Session, Participant
from model_utils.models import TimeStampedModel


@python_2_unicode_compatible
class UserParticipantAssociation(models.Model):
    user = models.OneToOneField(User)
    session = models.ForeignKey(Session, null=True)
    session_name = models.CharField(max_length=255)
    participant = models.OneToOneField(Participant, null=True)
    money_earned = models.DecimalField(default=0, max_digits=6, decimal_places=2)
    # consent = models.NullBooleanField(null=True)

    def __str__(self):
        return u'user={} session={}-{} participant={}'.format(self.user.username, self.session, self.session_name,
                                                              self.participant)
