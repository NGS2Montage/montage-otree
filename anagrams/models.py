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
    num_groups = 1
    num_rounds = 1
    letter_distribution = [["a", 46], ["b", 10], ["c", 22], ["d", 19], ["e", 59], ["f", 6], ["g", 13], ["h", 14],
                           ["i", 46], ["j", 1], ["k", 4], ["l", 30], ["m", 15], ["n", 38], ["o", 38], ["p", 16],
                           ["q", 1], ["r", 38], ["s", 38], ["t", 34], ["u", 19], ["v", 5], ["w", 4], ["x", 1],
                           ["y", 10], ["z", 2]]

class Subsession(BaseSubsession):
    def before_session_starts(self):   # called each round
        """For each player, create a fixed number of "decision stubs" with random values to be decided upon later."""
        if 'threshold_stop_game_num_words' not in self.session.config:
            self.session.config['threshold_stop_game_num_words'] = 400

        if self.round_number == 1:

            # extract and mix the players
            players = self.get_allowed_players()
            
            # random.shuffle(players)

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


        for p in players:
            p.generate_user_letters()
            p.word_channel = p.get_word_channel()
            p.save()

            
    def get_allowed_players(self):
        players = []
        for player in self.get_players():
            ###############################
            ## Development only!            
            ###############################
            # player.participant.vars['consent'] = True
            # player.participant.vars['playing'] = True

            ###############################

            if player.participant.vars['consent'] and player.participant.vars['playing']:
                players.append(player)
        return players

    def calculate_team_score(self):
        
        total_words = self.n_words + self.n_duplicates
        word_threshold = self.session.config['threshold_num_words']
        
        if total_words < word_threshold:
            return (0, False, 0, 0)
        
        # Threshold
        score = self.session.config['threshold_num_points']
        
        # Marginal Score
        score_marginal = max([self.n_words - word_threshold, 0]) * self.session.config['marginal_points']
        score += score_marginal
        
        # Duplicate Score
        score_duplicate = self.n_duplicates * self.session.config['marginal_points'] * 2
        score += score_duplicate
        
        return (score, True, score_marginal, score_duplicate)
    
    def set_payoffs(self):
        
        allowed_players = self.get_allowed_players()
        
        # Get total words:
        word_objects = TeamWord.objects.filter(group=allowed_players[0].group)
        
        self.n_words = len(set(word_objects.values_list('word', flat=True)))
        self.n_duplicates = len(word_objects.values_list('word', flat=True)) - self.n_words
        self.n_players = len(allowed_players)
        
        if self.n_players > 0:
            payoff = self.calculate_team_score()[0] / self.n_players
            for p in allowed_players:
                p.payoff = payoff
    
    
    n_words = models.IntegerField()
    n_duplicates = models.IntegerField()
    n_players = models.IntegerField()

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    neighbors = django_models.ManyToManyField('Player')
    word_channel = django_models.CharField(max_length=255)

    # Difi Index Columns
    distanceScale_after = models.IntegerField()
    overlapScale_after = models.IntegerField()

    def generate_user_letters(self):
        # alphabet = list(string.ascii_lowercase)
        distributed_letters = []
        generated = set()
        for ltr, num in Constants.letter_distribution:
            for i in range(num):
                distributed_letters.append(ltr)
        for _ in range(self.session.config['n_letters']):
            letter = self.userletter_set.create()
            found = False
            while not found:
                letter_choice = random.choice(distributed_letters).upper()
                if letter_choice in generated:
                    continue
                generated.add(letter_choice)
                found = True
            letter.letter = letter_choice
            letter.save()

    def get_transaction_channel(self):
        return '{}-transaction-{}-{}'.format(
            Constants.name_in_url,
            self.session.id,
            self.participant.code
        )

    def get_word_channel(self):
        return 'word-{}-{}-{}'.format(
            self.session.id,
            Constants.name_in_url,
            self.group.id
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
    approve_time = models.FloatField()
    channel = models.CharField(max_length=255)
    owner_channel = models.CharField(max_length=255)
    timestamp = models.FloatField(default=time.time)

    def to_dict(self):
        return {
            'letter': self.letter.letter,
            'owner': self.letter.player.chat_nickname(),
            'borrower': self.player.chat_nickname(),
            'pk': self.pk,
            'approved': self.approved,
        }


class ChatGroup(django_models.Model):
    players = django_models.ManyToManyField('Player')


class TeamWord(models.Model):
    class Meta:
        index_together = ['channel', 'timestamp']

    # the name "channel" here is unrelated to Django channels
    channel = models.CharField(max_length=255)
    player = models.ForeignKey(Player)
    group = models.ForeignKey(Group)

    word = models.CharField(max_length=100)
    timestamp = models.FloatField(default=time.time)


class Dictionary(models.Model):
    word = models.CharField(max_length=100, db_index=True, unique=True)
    # word = models.CharField(max_length=100)
