from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Parang Saraf'

doc = """
This app implements the Group Ultimatum Game
"""


class Constants(BaseConstants):
    name_in_url = 'phase3'
    players_per_group = 4
    num_rounds = 1

    endowment = c(100)


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for p in self.get_players():
            if p.id_in_group % 2 == 0:
                p.player_role = 'receiver'
            else:
                p.player_role = 'offeror'


class Group(BaseGroup):
    offerors_average = models.CurrencyField()
    receivers_average = models.CurrencyField()

    def set_payoff(self):
        offeror_sum, offeror_count, receiver_sum, receiver_count = 0, 0, 0, 0
        for p in self.get_players():
            if p.player_role == 'offeror':
                offeror_sum += p.offered_amount
                offeror_count += 1
            else:
                receiver_sum += p.receiver_expectation
                receiver_count += 1
        self.offerors_average = offeror_sum / offeror_count
        self.receivers_average = receiver_sum / receiver_count
        if self.offerors_average >= self.receivers_average:
            payoff = self.offerors_average
        else:
            payoff = c(0)
        for p in self.get_players():
            if payoff == c(0):
                p.payoff = 0
                continue
            if p.player_role == 'offeror':
                p.payoff = Constants.endowment - payoff
            else:
                p.payoff = payoff


class Player(BasePlayer):

    initial_offered_amount = models.CurrencyField(min=c(0), max=c(Constants.endowment))
    initial_receiver_expectation = models.CurrencyField(min=c(0), max=c(Constants.endowment))
    offered_amount = models.CurrencyField(min=c(0), max=c(Constants.endowment))
    receiver_expectation = models.CurrencyField(min=c(0), max=c(Constants.endowment))
    player_role = models.CharField(choices=['offeror', 'receiver'])

