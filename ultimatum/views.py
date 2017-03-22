from otree.api import Currency as c, currency_range
from django.contrib.auth.decorators import login_required
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, ChatGroup
from .social_graph import create_network
from django.core.mail import send_mail


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
    # timeout_seconds = 60
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
    form_fields = ['final_offered_amount']
    is_debug = False
    timeout_seconds = 30

    def is_displayed(self):
        return self.player.player_role == 'offeror'


class FinalExpectation(Page):
    form_model = models.Player
    form_fields = ['final_receiver_expectation']
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
    Offer,
    InitialResultsWaitPage,
    ShowOfferorBids,
    ShowReceiverBids,
    FinalOffer,
    FinalExpectation,
    FinalResultsWaitPage,
    Results,
    DifiIndex
]
