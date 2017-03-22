from ._builtin import WaitPage


class WaitPage(WaitPage):
    is_debug = False
    template_name = 'public_goods_waiting/WaitPage.html'

    def after_all_players_arrive(self):
        for participant in self.session.get_participants():
            if participant.vars['consent'] and participant.vars['playing']:
                participant.vars['locked'] = True
        self.session.vars['locked'] = True

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
