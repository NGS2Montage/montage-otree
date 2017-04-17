from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Parang Saraf'

doc = """
This app displays games instructions and quizes.
"""


class Constants(BaseConstants):
    name_in_url = 'instructions-pgg'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for p in self.get_players():
            
            # Saving correct solutions for Public Goods Game
            p.public_goods_question1_solution = "c__d__f"


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Public Goods game Quiz
    public_goods_question1 = models.CharField()
    public_goods_question1_solution = models.CharField(choices=["c__d__f"])
    public_goods_hidden = models.IntegerField()
    public_goods_score = models.IntegerField()
