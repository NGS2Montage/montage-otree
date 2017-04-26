from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)


author = 'Brian J. Goode'

doc = """
Ask random questions to players.
"""


class Constants(BaseConstants):
    name_in_url = 'prediction_phase'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    
    ruse_Q1 = models.CharField(
        verbose_name= """
        What is your favorite color? 
        """
        )

    ruse_Q2 = models.IntegerField(
        verbose_name="""
        What is your favorite number?
        """
        )

    ruse_Q3 = models.CharField(
        verbose_name="""
        What is your favorite movie?
        """
        )
