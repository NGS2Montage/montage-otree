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
            p.anagram_question1_solution = "a"
            p.anagram_question2_solution = "b"
            p.anagram_question3_solution = "a__b__c"
            p.anagram_question4_solution = "b"

            # Saving correct solutions for Public Goods Game
            p.public_goods_question1_solution = "c__d"

            # Saving correct solutions for Group Ultimatum Game
            p.ultimatum_question1_solution = "True"
            p.ultimatum_question2_solution = "b__c"
            p.ultimatum_question3_solution = "a__d"
            p.ultimatum_question4_solution = "b"
            p.ultimatum_question5_solution = "a"


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    # Anagram game Quiz
    anagram_question1 = models.CharField()
    anagram_question2 = models.CharField()
    anagram_question3 = models.CharField()
    anagram_question4 = models.CharField()

    anagram_question1_solution = models.CharField(choices=["a"])
    anagram_question2_solution = models.CharField(choices=["b"])
    anagram_question3_solution = models.CharField(choices=["a__b__c"])
    anagram_question4_solution = models.CharField(choices=["b"])
    anagram_hidden = models.IntegerField()
    anagram_score = models.IntegerField()

    # Public Goods game Quiz
    public_goods_question1 = models.CharField()
    public_goods_question1_solution = models.CharField(choices=["c__d"])
    public_goods_hidden = models.IntegerField()
    public_goods_score = models.IntegerField()

    # Ulitmatum game Quiz
    ultimatum_question1 = models.CharField(
        verbose_name="The Proposer Team is given [$10] and has to choose what percentage of the $10 to offer to the "
                     "other team (the Responder Team). Is this statement true or false?",
        choices=["True", "False"],
        widget=widgets.RadioSelect()
    )
    ultimatum_question2 = models.CharField()
    ultimatum_question3 = models.CharField()
    ultimatum_question4 = models.CharField()
    ultimatum_question5 = models.CharField()

    ultimatum_question1_solution = models.CharField(choices=["True"])
    ultimatum_question2_solution = models.CharField(choices=["b__c"])
    ultimatum_question3_solution = models.CharField(choices=["a__d"])
    ultimatum_question4_solution = models.CharField(choices=["b"])
    ultimatum_question5_solution = models.CharField(choices=["a"])
    ultimatum_hidden = models.IntegerField()
    ultimatum_score = models.IntegerField()

