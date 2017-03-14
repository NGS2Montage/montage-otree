from otree.api import Currency as c, currency_range
from django.contrib.auth.decorators import login_required
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class DifiIndex(LoginRequiredMixin, Page):
    is_debug = False
    form_model = models.Player
    form_fields = ['distanceScale', 'overlapScale']


class Contribute(LoginRequiredMixin, Page):
    form_model = models.Player
    form_fields = ['contribution']
    is_debug = False
    timeout_seconds = 20
    timeout_submission = {'contribution': 0.0}


class Results(LoginRequiredMixin, Page):
    is_debug = False
    pass


class ResultsWaitPage(LoginRequiredMixin, WaitPage):
    is_debug = False

    def after_all_players_arrive(self):
        self.group.set_payoffs()


page_sequence = [
    DifiIndex,
    Contribute,
    ResultsWaitPage,
    Results
]
