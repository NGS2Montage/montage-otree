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


class WaitPage(WaitPage):
    is_debug = False
    template_name = 'public_goods/WaitPage.html'

    def after_all_players_arrive(self):
        for participant in self.session.get_participants():
            if participant.vars['consent'] and participant.vars['playing']:
                participant.vars['locked'] = True
        self.session.vars['locked'] = True


class Contribute(Page):
    form_model = models.Player
    form_fields = ['contribution']
    is_debug = False
    timeout_seconds = Constants.decision_time_min * 60;
    timeout_submission = {'contribution': -1}

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and self.participant.vars['locked']:
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened and self.player.contribution < 0:
                self.participant.vars['playing'] = False

    def contribution_min(self):
        return 0

    def contribution_max(self):
        return Constants.endowment

    def contribution_error_message(self, value):
        if value < 0:
            return "Must select a value between 0 and %d" % Constants.endowment
        if value > Constants.endowment:
            return "Must select a value between 0 and %d" % Constants.endowment

    def vars_for_template(self):
        return {
            'nPlayers': len(self.player.get_others_in_group()) + 1,
            }

class ResultsWaitPage(WaitPage):
    is_debug = False

    def after_all_players_arrive(self):
        self.subsession.set_payoffs()

    '''
    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and self.participant.vars['locked']:
            return True
        else:
            return False
    '''


class Results(Page):
    is_debug = False

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and self.participant.vars['locked']:
            return True
        else:
            return False


class NoResponse(Page):
    is_debug = False

    def is_displayed(self):
        if self.participant.vars['consent'] and not self.participant.vars['playing'] and self.participant.vars['locked']:
            return True
        else:
            return False


class DifiIndex(Page):
    is_debug = False
    form_model = models.Player
    form_fields = ['distanceScale', 'overlapScale']

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and self.participant.vars['locked']:
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False


page_sequence = [
    WaitPage,
    Contribute,
    ResultsWaitPage,
    NoResponse,
    DifiIndex,
]
