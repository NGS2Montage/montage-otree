from ._builtin import WaitPage


class WaitPage(WaitPage):
    is_debug = False
    template_name = 'public_goods_waiting/WaitPage.html'

    def after_all_players_arrive(self):
        pass


page_sequence = [
    WaitPage,
]
