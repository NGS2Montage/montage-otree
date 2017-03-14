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
    players_per_group = 2
    num_rounds = 1
    endowment = c(100)
    efficiency_factor = 2


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_contribution = models.CurrencyField()
    individual_share = models.CurrencyField()

    def set_payoffs(self):
        self.total_contribution = sum([p.contribution for p in self.get_players()])
        self.individual_share = self.total_contribution * Constants.efficiency_factor / Constants.players_per_group
        for p in self.get_players():
            p.payoff = Constants.endowment - p.contribution + self.individual_share
            p.profit = p.payoff - Constants.endowment


class Player(BasePlayer):

    # Difi Index Columns
    distanceScale = models.IntegerField()
    overlapScale = models.IntegerField()

    contribution = models.CurrencyField(min=0, max=Constants.endowment)
    profit = models.CurrencyField(min=0)

