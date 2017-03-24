from otree.api import Currency as c, currency_range, safe_json
from . import models
from ._builtin import Page, WaitPage
from .models import Constants, ChatGroup
from ultimatum.social_graph import create_network


class WaitPage(WaitPage):
    is_debug = False
    template_name = 'anagrams/WaitPage.html'

    def after_all_players_arrive(self):
        group_size = Constants.num_neighbors;
        for group in self.subsession.get_groups():
            self.assign_players_in_chatgroups(group.get_players(), group_size)

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


class Anagrams(Page):

    def vars_for_template(self):
        context = {}

        letters = {
            self.player.chat_nickname(): [{'letter': ul.letter, 'pk': ul.pk} for ul in self.player.userletter_set.all()]
        }
        for neighbor in self.player.neighbors.all():
            letters[neighbor.chat_nickname()] = [{'letter': ul.letter, 'pk': ul.pk} for ul in neighbor.userletter_set.all()]


        context['word_channel'] = 'word-{}-{}-{}'.format(
                self.session.id,
                Constants.name_in_url,
                self.group.id
            )

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

    def after_all_players_arrive(self):
        pass


class Results(Page):
    pass


page_sequence = [
    WaitPage,
    Anagrams,
    ResultsWaitPage,
    Results
]
