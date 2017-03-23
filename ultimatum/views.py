from otree.api import Currency as c, currency_range
from django.contrib.auth.decorators import login_required
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, ChatGroup
from .social_graph import create_network
from django.core.mail import send_mail
from otree.api import safe_json


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class WaitPage(WaitPage):
    is_debug = False
    template_name = 'ultimatum/WaitPage.html'

    def after_all_players_arrive(self):
        eligible_players = []
        self.session.vars['locked'] = True
        for player in self.subsession.get_players():
            if player.participant.vars['consent'] and player.participant.vars['playing']:
                player.participant.vars['locked'] = True
                eligible_players.append(player)

        # The initial role assignment is written in ultimatum/models.py before_session_starts. However, since players
        # might drop, this reassigns the roles to balance out the teams after phase 1 and 2 has been played
        offerors, receivers = [], []
        group_size = self.session.config['ultimatum_group_size']
        if self.session.config['ultimatum_split']:
            for num, player in enumerate(eligible_players):
                if num % 2 == 0:
                    player.player_role = 'offeror'
                    player.save()
                    offerors.append(player)
                else:
                    player.player_role = 'receiver'
                    player.save()
                    receivers.append(player)
            self.assign_players_in_chatgroups(offerors, group_size)
            self.assign_players_in_chatgroups(receivers, group_size)
        else:
            role = self.session.config['ultimatum_player_role']
            role_players = []
            for player in eligible_players:
                player.player_role = role
                player.save()
                role_players.append(player)
            self.assign_players_in_chatgroups(role_players, group_size)

    def assign_players_in_chatgroups(self, players, group_size):
        if group_size < 2:
            self.send_error_email("Group Size was: %d" % group_size)
            return
        if len(players) < group_size + 1:
            self.send_error_email("Number of Players were: %d\nGroup Size was: %d" % (len(players), group_size))
            return

        success, groups = create_network(len(players), group_size, 55, 2, False, False, './')
        if not success:
            self.send_error_email("Number of Players were: %d\nGroup Size was: %d" % (len(players), group_size))
            return

        for grp in groups:
            grpObj = ChatGroup.objects.create()
            grpObj.players.add(players[grp])
            for id in groups[grp]:
                players[grp].neighbors.add(players[id])
                grpObj.players.add(players[id])
            players[grp].save()
            grpObj.save()

    def send_error_email(self, message, subject="Error Creating Neighbors Network"):
        send_mail(subject=subject, message=message, from_email='NGS2 Montage <ngs2.montage@gmail.com>',
                  recipient_list=['parang.saraf@gmail.com'], fail_silently=True)


class Offer(Page):
    form_model = models.Player
    form_fields = ['initial_offered_amount', 'initial_receiver_expectation']
    is_debug = False
    template_name = 'ultimatum/offer.html'
    timeout_seconds = 180
    timeout_submission = {'initial_offered_amount': -1, 'initial_receiver_expectation': Constants.endowment + 10}

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and self.participant.vars['locked']:
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened and (
                        self.player.initial_offered_amount < 0 or self.player.initial_receiver_expectation > Constants.endowment):
            self.participant.vars['playing'] = False

    def initial_offered_amount_min(self):
        return 0

    def initial_offered_amount_max(self):
        return Constants.endowment

    def initial_receiver_expectation_min(self):
        return 0

    def initial_receiver_expectation_max(self):
        return Constants.endowment


class InitialResultsWaitPage(WaitPage):
    template_name = 'ultimatum/initial_results_wait.html'
    is_debug = False


class ShowOfferorBids(Page):
    is_debug = False
    timeout_seconds = 180
    show_histogram = False

    def vars_for_template(self):
        neighbors = []
        for player in self.player.neighbors.all():
            if player.participant.vars['playing']:
                expectation = "Player %d is offering %d" % (player.id, player.initial_offered_amount)
                neighbors.append({'offer': expectation, 'neighbor_id': player.id, 'user_id': self.player.id})

        if self.session.config['ultimatum_histogram']:
            self.show_histogram = True
            bids = []
            for player in self.group.get_players():
                if player.participant.vars['consent'] and player.participant.vars['playing'] and \
                        player.participant.vars['locked'] and player.player_role == 'offeror':
                    bids.append(player.initial_offered_amount)
            labels, values = create_histogram(bids)
            return {'neighbors': neighbors, 'labels': safe_json(labels), 'values': safe_json(values)}
        return {'neighbors': neighbors}

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                self.participant.vars['locked'] and self.player.player_role == 'offeror':
            return True
        else:
            return False


def create_histogram(bids):
    hist = {}
    for maximum in range(10, 110, 10):
        minimum = maximum - 10
        if maximum == 100:
            maximum = 101
        label = "%d-%d" % (minimum, maximum - 1)
        hist[label] = 0
        for bid in bids:
            if minimum <= bid < maximum:
                hist[label] += 1
    labels, values = [], []
    for label in sorted(hist):
        labels.append(label)
        values.append(hist[label])
    return labels, values


class ShowReceiverBids(Page):
    is_debug = False
    timeout_seconds = 180
    show_histogram = False

    def vars_for_template(self):
        neighbors = []
        for player in self.player.neighbors.all():
            if player.participant.vars['playing']:
                expectation = "Player %d expects to receive %d" % (player.id, player.initial_receiver_expectation)
                neighbors.append({'expectation': expectation, 'neighbor_id': player.id, 'user_id': self.player.id})

        if self.session.config['ultimatum_histogram']:
            self.show_histogram = True
            bids = []
            for player in self.group.get_players():
                if player.participant.vars['consent'] and player.participant.vars['playing'] and \
                        player.participant.vars['locked'] and player.player_role == 'receiver':
                    bids.append(player.initial_receiver_expectation)
            labels, values = create_histogram(bids)
            return {'neighbors': neighbors, 'labels': safe_json(labels), 'values': safe_json(values)}
        return {'neighbors': neighbors}

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                self.participant.vars['locked'] and self.player.player_role == 'receiver':
            return True
        else:
            return False


class FinalOffer(Page):
    form_model = models.Player
    form_fields = ['final_offered_amount']
    is_debug = False
    timeout_seconds = 180
    timeout_submission = {'final_offered_amount': -1}

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                self.participant.vars['locked'] and self.player.player_role == 'offeror':
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened and self.player.final_offered_amount < 0:
            self.participant.vars['playing'] = False

    def final_offered_amount_min(self):
        return 0

    def final_offered_amount_max(self):
        return Constants.endowment


class FinalExpectation(Page):
    form_model = models.Player
    form_fields = ['final_receiver_expectation']
    is_debug = False
    timeout_seconds = 180
    timeout_submission = {'final_receiver_expectation': Constants.endowment + 10}

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                self.participant.vars['locked'] and self.player.player_role == 'receiver':
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened and self.player.final_receiver_expectation > Constants.endowment:
            self.participant.vars['playing'] = False

    def final_receiver_expectation_min(self):
        return 0

    def final_receiver_expectation_max(self):
        return Constants.endowment


class FinalResultsWaitPage(WaitPage):
    is_debug = False
    template_name = 'ultimatum/initial_results_wait.html'

    def after_all_players_arrive(self):
        self.subsession.set_payoff()


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


class ThankYou(Page):
    is_debug = False


page_sequence = [
    WaitPage,
    Offer,
    InitialResultsWaitPage,
    ShowOfferorBids,
    ShowReceiverBids,
    FinalOffer,
    FinalExpectation,
    FinalResultsWaitPage,
    Results,
    DifiIndex,
    ThankYou
]
