from django.db import models
from otree.models import Participant
import time

class Click(models.Model):
    participant = models.ForeignKey(Participant)
    timestamp = models.FloatField(default=time.time)
    element = models.CharField(max_length=255)
