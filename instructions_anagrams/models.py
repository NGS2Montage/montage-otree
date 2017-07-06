from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Parang Saraf'

doc = """
This app displays games instructions and quizes.
"""


class Constants(BaseConstants):
    name_in_url = 'instructions'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    def before_session_starts(self):
        for p in self.get_players():
            # Saving correct solutions for Anagram Game
            p.anagram_question1_solution = "a__d"

class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Anagram game Quiz
    anagram_question1 = models.CharField()

    # Difi Index Columns
    distanceScale_before = models.IntegerField()
    overlapScale_before = models.IntegerField()
    
    anagram_question1_solution = models.CharField(choices=["a__d"])
    anagram_hidden = models.IntegerField()
    anagram_score = models.IntegerField()
