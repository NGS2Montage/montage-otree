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
        Sports: Which NBA team in the United States do you think will 
        win the Championship Title in 2017? 
        """
        )

    ruse_Q2 = models.IntegerField(
        verbose_name="""
        Economy: In how many years will there be another stock
        market crash on the New York Stock Exchange (NYSE)?
        """
        )

    ruse_Q3 = models.CharField(
        verbose_name="""
        Travel: Which city will be ranked the #1 most livable city
        based on the "livability" index in the year 2017?
        """
        )
