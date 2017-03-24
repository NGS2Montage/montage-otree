from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from otree.db.models import Model, ForeignKey

from django.db import models as django_models

import random
import string
import time

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'anagrams'
    players_per_group = None
    num_groups = 2
    num_rounds = 1
    num_user_letters = 3
    num_neighbors = 2


class Subsession(BaseSubsession):
    def before_session_starts(self):   # called each round
        """For each player, create a fixed number of "decision stubs" with random values to be decided upon later."""
        for p in self.get_players():
            p.generate_user_letters()

        if self.round_number == 1:

            # extract and mix the players
            players = self.get_players()
            random.shuffle(players)

            # create the base for number of groups
            num_players = len(players)

            # create a list of how many players must be in every group
            # the result of this will be [2, 2, 2, 2, 2, 2, 2, 2]
            # obviously 2 * 8 = 16
            # ppg = 'players per group'
            ppg_list = [num_players // Constants.num_groups] * Constants.num_groups

            # add one player in order per group until the sum of size of
            # every group is equal to total of players
            i = 0
            while sum(ppg_list) < num_players:
                ppg_list[i] += 1
                i += 1
                if i >= len(ppg_list):
                    i = 0

            # reassignment of groups
            list_of_lists = []
            for j, ppg in enumerate(ppg_list):
                # it is the first group the start_index is 0 otherwise we start
                # after all the players already exausted
                start_index = 0 if j == 0 else sum(ppg_list[:j])

                # the asignation of this group end when we asign the total
                # size of the group
                end_index = start_index + ppg

                # we select the player to add
                group_players = players[start_index:end_index]
                list_of_lists.append(group_players)
            self.set_group_matrix(list_of_lists)
        else:
            self.group_like_round(1)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    neighbors = django_models.ManyToManyField('Player')

    def generate_user_letters(self):
        alphabet = list(string.ascii_lowercase)
        for _ in range(Constants.num_user_letters):
            letter = self.userletter_set.create()
            letter.letter = random.choice(alphabet)
            letter.save()

    def get_transaction_channel(self):
        return '{}-transaction-{}-{}'.format(
            Constants.name_in_url,
            self.session.id,
            self.participant.code
        )

    def chat_nickname(self):
        return 'Player {}'.format(self.id_in_group)

    def chats(self):
        channels = []
        for other in self.neighbors.all():
            if other.id_in_group < self.id_in_group:
                lower_id, higher_id = other.id_in_group, self.id_in_group
            else:
                lower_id, higher_id = self.id_in_group, other.id_in_group
            channels.append({
                # make a name for the channel that is the same for all
                # channel members. That's why we order it (lower, higher)
                'channel': '{}-{}-{}'.format(self.group.id, lower_id, higher_id),
                'label': 'Chat with {}'.format(other.chat_nickname())
            })
        return channels


class UserLetter(Model):
    letter = models.CharField(max_length=1)
    player = ForeignKey(Player)


class LetterTransaction(models.Model):
    class Meta:
        index_together = ['channel', 'timestamp']

    player = ForeignKey(Player)  # this is the borrower
    letter = ForeignKey(UserLetter)
    approved = models.BooleanField(default=False)

    channel = models.CharField(max_length=255)
    timestamp = models.FloatField(default=time.time)


class ChatGroup(django_models.Model):
    players = django_models.ManyToManyField('Player')


class TeamWord(models.Model):
    class Meta:
        index_together = ['channel', 'timestamp']

    # the name "channel" here is unrelated to Django channels
    channel = models.CharField(max_length=255)
    group = models.ForeignKey(Group)

    word = models.CharField(max_length=100)
    timestamp = models.FloatField(default=time.time)


class Dictionary(models.Model):
    word = models.CharField(max_length=100, db_index=True, unique=True)
