from __future__ import unicode_literals


from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible


from model_utils import Choices
from model_utils.models import TimeStampedModel

from .managers import GameManager


@python_2_unicode_compatible
class Game(TimeStampedModel):
    # STATE = Choices('w1', 'g1', 'w2', 'g2', 'w3', 'g31', 'g32', 'g33')
    # state = models.CharField(choices=STATE, default=STATE.w1, max_length=20)
    game_code = models.CharField(max_length=20)
    state = models.ForeignKey('GameStates')
    objects = GameManager()

    def __str__(self):
        return u'game={} state={}'.format(self.game_code, self.state)

    # def advance_to_next_state(self):
    #     if self.state == 'w1':
    #         # create teams
    #         # create groups
    #         # assign anagram letters -> this function should be somewhere in
    #         #   anagrams dir
    #         # advance all users at state w1 to g1
    #         self.state = 'g1'
    #         self.save()


@python_2_unicode_compatible
class GameStates(models.Model):
    state_code = models.CharField(max_length=30, unique=True)
    state_name = models.CharField(max_length=100)
    order = models.IntegerField(unique=True)
    allowed_user_states = models.ManyToManyField('GameStates', related_name='allowed_states_admin')
    url_name = models.CharField(max_length=200)

    def __str__(self):
        return self.state_code


@python_2_unicode_compatible
class Team(models.Model):
    offeror = models.BooleanField(default=False)
    game = models.ForeignKey(Game, null=True, on_delete=models.CASCADE)

    def __str__(self):
        # Is this confusing? We use this elsewhere as the channels Group name
        # for the whole team, maybe we should have a group_name() function on
        # this model to be more explicit?
        return 'team-{}'.format(self.pk)


@python_2_unicode_compatible
class Group(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return "group-{}".format(self.user.username)


@python_2_unicode_compatible
class Profile(TimeStampedModel):
    # STATE = Choices('s1', 't1', 'w1', 'g1', 'g2', 's2', 't2', 'w3', 's3', 't3', 'g31', 'g32', 'g33')

    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)

    #state = models.CharField(choices=STATE, default=STATE.s1, max_length=20)
    state = models.ForeignKey('GameStates')
    game = models.ForeignKey('Game')
    groups = models.ManyToManyField(Group)
    money_earned = models.DecimalField(default=0, max_digits=6, decimal_places=2)

    def __str__(self):
        return u'user={} state={}'.format(self.user.username, self.state)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(
            user=instance, 
            state=GameStates.objects.get(state_code="pre"),
            game=Game.objects.all()[0])
        profile.groups.create(user=instance)


@python_2_unicode_compatible
class ChatMessage(TimeStampedModel):
    message = models.TextField()
    room = models.CharField(max_length=200)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return u'[{}] {} (room: {})'.format(self.user.username, self.message, self.room)
