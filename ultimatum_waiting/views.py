from ._builtin import WaitPage


class WaitPage(WaitPage):
    is_debug = False
    template_name = 'ultimatum_waiting/WaitPage.html'

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        elif not self.participant.vars['clicked']:
            return True
        else:
            return False

    def after_all_players_arrive(self):
        pass


page_sequence = [
    WaitPage,
]
