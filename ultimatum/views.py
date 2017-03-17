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


class Offer(Page):
    form_model = models.Player
    form_fields = ['initial_offered_amount', 'initial_receiver_expectation']
    is_debug = False
    template_name = 'ultimatum/offer.html'
    timeout_seconds = 300
    timeout_submission = {'initial_offered_amount': 0, 'initial_receiver_expectation': 100}

    def get(self, request, *args, **kwargs):
        print(self.player.player_role)
        return super(Offer, self).get(request, args, kwargs)


class InitialResultsWaitPage(WaitPage):
    is_debug = False


class ShowOfferorBids(Page):
    is_debug = False
    timeout_seconds = 300
    template_name = 'ultimatum/offeror_distribution.html'

    def vars_for_template(self):
        bids = []
        for p in self.group.get_players():
            if p == self.player:
                continue
            if p.player_role == 'offeror':
                offer = "Player %d: %d" % (p.id_in_group, p.initial_offered_amount)
                bids.append({'offer': offer, 'offeror_id': p.id_in_group, 'user_id': self.player.id_in_group})
        return {'bids': bids}

    def is_displayed(self):
        return self.player.player_role == 'offeror'


class ShowReceiverBids(Page):
    is_debug = False
    timeout_seconds = 300

    def vars_for_template(self):
        bids = []
        for p in self.group.get_players():
            if p == self.player:
                continue
            if p.player_role == 'receiver':
                expectation = "Player %d: %d" % (p.id_in_group, p.initial_receiver_expectation)
                bids.append({'expectation': expectation, 'offeror_id': p.id_in_group,
                             'user_id': self.player.id_in_group})
        return {'bids': bids}

    def is_displayed(self):
        return self.player.player_role == 'receiver'


class FinalOffer(Page):
    form_model = models.Player
    form_fields = ['offered_amount']
    is_debug = False
    timeout_seconds = 30

    def is_displayed(self):
        return self.player.player_role == 'offeror'


class FinalExpectation(Page):
    form_model = models.Player
    form_fields = ['receiver_expectation']
    is_debug = False
    timeout_seconds = 30

    def is_displayed(self):
        return self.player.player_role == 'receiver'



class FinalResultsWaitPage(WaitPage):
    is_debug = False

    def after_all_players_arrive(self):
        self.group.set_payoff()


class Results(Page):
    pass


page_sequence = [
    Offer,
    InitialResultsWaitPage,
    ShowOfferorBids,
    ShowReceiverBids,
    FinalOffer,
    FinalExpectation,
    FinalResultsWaitPage,
    Results
]
