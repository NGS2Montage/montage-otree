from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, ChatGroup, TeamWord
from ultimatum.social_graph import create_network
from django.core.mail import send_mail


class WaitPage(WaitPage):
    is_debug = False
    template_name = 'anagrams/WaitPage.html'

    def after_all_players_arrive(self):
        group_size = Constants.num_neighbors
        for group in self.subsession.get_groups():
            self.assign_players_in_chatgroups(group.get_players(), group_size)
        '''
        eligible_players = []
        self.session.vars['locked'] = True
        for player in self.subsession.get_players():
            if player.participant.vars['consent'] and player.participant.vars['playing']:
                player.participant.vars['locked'] = True
                eligible_players.append(player)

        num_players = len(eligible_players)
        ppg_list = [num_players // Constants.num_groups] * Constants.num_groups

        i = 0
        while sum(ppg_list) < num_players:
            ppg_list[i] += 1
            i += 1
            if i >= len(ppg_list):
                i = 0

        # reassignment of groups
        list_of_lists = []
        for j, ppg in enumerate(ppg_list):
            start_index = 0 if j == 0 else sum(ppg_list[:j])
            end_index = start_index + ppg
            group_players = eligible_players[start_index:end_index]
            list_of_lists.append(group_players)
        uneligible_players = []
        for p in self.subsession.get_players():
            if p not in eligible_players:
                uneligible_players.append(p)
        list_of_lists.append(uneligible_players)
        self.subsession.set_group_matrix(list_of_lists)

        for p in eligible_players:
            p.generate_user_letters()
            p.word_channel = p.get_word_channel()
            p.save()
        '''

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

    def vars_for_template(self):
        return {
        'nPlayers': 1 + len(self.player.get_others_in_group()),
        }

class Anagrams(Page):
    is_debug = False
    timeout_seconds = Constants.anagrams_duration_sec

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

    def vars_for_template(self):
        context = {}

        letters = {
            self.player.chat_nickname(): [{'letter': ul.letter, 'pk': ul.pk} for ul in self.player.userletter_set.all()]
        }
        for neighbor in self.player.neighbors.all():
            letters[neighbor.chat_nickname()] = [{'letter': ul.letter, 'pk': ul.pk} for ul in neighbor.userletter_set.all()]


        context['word_channel'] = self.player.get_word_channel()
        context['transaction_channel'] = self.player.get_transaction_channel()

        vars_for_js = {
            'participant_code': self.participant.code,
            'nickname': self.player.chat_nickname(),
            'letters': letters,
            'group': self.group.id,
            'word_channel': context['word_channel'],
            'transaction_channel': context['transaction_channel'],
        }

        context['vars_for_js'] = safe_json(vars_for_js)
        return context


class ResultsWaitPage(WaitPage):
    is_debug = False
    template_name = 'anagrams/initial_results_wait.html'

    def after_all_players_arrive(self):
        pass


class Results(Page):
    is_debug = False

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

    def vars_for_template(self):
        word_count = len(TeamWord.objects.filter(group=self.group))
        n_players = len(self.player.get_others_in_group()) + 1
        earnings_per_word = 1
        total_earnings = word_count * earnings_per_word
        toReturn = {'word_count': word_count, 'earnings_per_word': earnings_per_word,
                    'total_earnings': total_earnings, 'individual_earnings':
                    total_earnings / float(n_players)}
        return toReturn


class DifiIndexBefore(Page):
    is_debug = False
    form_model = models.Player
    form_fields = ['distanceScale_before', 'overlapScale_before']

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False


class DifiIndexAfter(Page):
    is_debug = False
    form_model = models.Player
    form_fields = ['distanceScale_after', 'overlapScale_after']

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False


page_sequence = [
    DifiIndexBefore,
    WaitPage,
    Anagrams,
    ResultsWaitPage,
    Results,
    DifiIndexAfter,
]
