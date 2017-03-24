from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from django.db import models as django_models


author = 'Parang Saraf'

doc = """
This app implements the Group Ultimatum Game
"""


class Constants(BaseConstants):
    name_in_url = 'phase3'
    players_per_group = None
    num_rounds = 1
    endowment = 100


class Subsession(BaseSubsession):
    offerors_average = models.FloatField()
    receivers_average = models.FloatField()

    def before_session_starts(self):
        for p in self.get_players():
            if p.id_in_group % 2 == 0:
                p.player_role = 'receiver'
            else:
                p.player_role = 'offeror'

    def get_allowed_players(self):
        players = []
        for player in self.get_players():
            if player.participant.vars['consent'] and player.participant.vars['playing'] and \
                    player.participant.vars['locked']:
                players.append(player)
        return players

    def set_payoff(self):
        offeror_sum, offeror_count, receiver_sum, receiver_count = 0, 0, 0, 0
        allowed_players = self.get_allowed_players()
        for p in allowed_players:
            if p.player_role == 'offeror':
                offeror_sum += p.final_offered_amount
                offeror_count += 1
            else:
                receiver_sum += p.final_receiver_expectation
                receiver_count += 1

        if offeror_count == 0:
            self.offerors_average = 0
        else:
            self.offerors_average = offeror_sum / offeror_count
        if receiver_count == 0:
            self.receivers_average = 100
        else:
            self.receivers_average = receiver_sum / receiver_count

        if not self.session.config['ultimatum_split']:
            if self.session.config['ultimatum_player_role'] == 'receiver':
                self.offerors_average = self.session.config['ultimatum_cutoff']
            else:
                self.receivers_average = self.session.config['ultimatum_cutoff']

        if self.offerors_average >= self.receivers_average:
            payoff = self.offerors_average
        else:
            payoff = 0
        for p in allowed_players:
            if payoff == 0:
                p.payoff = 0
                continue
            if p.player_role == 'offeror':
                p.payoff = Constants.endowment - payoff
            else:
                p.payoff = payoff


class Group(BaseGroup):
    pass


class ChatGroup(django_models.Model):
    players = django_models.ManyToManyField('Player')



class Player(BasePlayer):
    initial_offered_amount = models.IntegerField(min=-1, max=Constants.endowment + 10)
    initial_receiver_expectation = models.IntegerField(min=-1, max=Constants.endowment + 10)
    final_offered_amount = models.IntegerField(min=-1, max=Constants.endowment + 10)
    final_receiver_expectation = models.IntegerField(min=-1, max=Constants.endowment + 10)
    player_role = models.CharField(choices=['offeror', 'receiver'])
    neighbors = django_models.ManyToManyField('Player')

    # Difi Index Columns
    distanceScale = models.IntegerField()
    overlapScale = models.IntegerField()

    def nickname(self):
        return 'Player {}'.format(self.id)

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
                'label': 'Chat with {}'.format(other.nickname())
            })
        return channels
