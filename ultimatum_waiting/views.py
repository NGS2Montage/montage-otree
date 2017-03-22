from ._builtin import WaitPage
from ultimatum.models import Player, ChatGroup
from .social_graph import create_network
from django.core.mail import send_mail


class WaitPage(WaitPage):
    is_debug = False
    template_name = 'ultimatum_waiting/WaitPage.html'

    def after_all_players_arrive(self):
        eligible_players = []
        self.session.vars['locked'] = True
        for participant in self.session.get_participants():
            if participant.vars['consent'] and participant.vars['playing']:
                participant.vars['locked'] = True
                try:
                    player = Player.objects.get(participant=participant)
                except Exception as e:
                    continue
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

    '''
    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        elif not self.participant.vars['clicked']:
            return True
        else:
            return False
    '''


page_sequence = [
    WaitPage,
]
