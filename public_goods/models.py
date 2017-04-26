from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Parang Saraf'

doc = """
This app displays the Public Goods Game
"""


class Constants(BaseConstants):
    name_in_url = 'phase2'
    players_per_group = None
    num_rounds = 1
    endowment = 100
    efficiency_factor = 2.0
    decision_time_min = 3


class Subsession(BaseSubsession):
    total_contribution = models.PositiveIntegerField()
    individual_share = models.FloatField()

    def get_allowed_players(self):
        players = []
        for player in self.get_players():
            if player.participant.vars['consent'] and player.participant.vars['playing']:
                players.append(player)
        return players

    def set_payoffs(self):
        allowed_players = self.get_allowed_players()
        if len(allowed_players) > 0:
            self.total_contribution = sum([p.contribution for p in allowed_players])
            self.individual_share = (self.total_contribution * Constants.efficiency_factor) / len(allowed_players)
        else:
            self.total_contribution = 0
            self.individual_share = 0
        for p in allowed_players:
            p.payoff = Constants.endowment - p.contribution + self.individual_share
            p.profit = p.payoff - Constants.endowment


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contribution = models.IntegerField(min=-1, max=Constants.endowment)
    profit = models.FloatField()

    # Difi Index Columns
    distanceScale = models.IntegerField()
    overlapScale = models.IntegerField()
