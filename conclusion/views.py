from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants
from otree.models_concrete import PageCompletion
import math

class Results(Page):
    
    is_debug = False
    timeout_seconds = 60
    
    def get_payoffs(self):
        to_display = {
            'anagrams': 'Anagrams Game', 
            'public_goods': 'Team Contribution Game', 
            'demographic_detailed': 'Optional Survey',
            'conclusion': 'Time on Wait Pages'
            }
        app_sequence = self.session.config['app_sequence']
        apps = [x for x in app_sequence if x in to_display]
        
        payoffs = []
        participant = self.participant
        total_pts = 0
        for app in apps:
            payoff = getattr(self.participant, '{}_player'.format(app)).first().payoff
            total_pts += payoff
            payoffs.append(
                {
                    'name': to_display[app],
                    'pay': payoff,
                })

        return payoffs
    
    def vars_for_template(self):
        total_wait_page_pts = 0
        for wait_page in self.session.config['paid_wait_pages']:
            try:
                pc = PageCompletion.objects.get(
                    app_name=wait_page[0],
                    page_name=wait_page[1],
                    participant_id=self.participant.id)

                payoff = math.ceil(pc.seconds_on_page * self.session.config['points_per_waiting_second'])
                print("{} seconds on {} pays {}".format(pc.seconds_on_page, wait_page, payoff))
                total_wait_page_pts += payoff

            except PageCompletion.DoesNotExist:
                print("No PageCompletion {} for {}".format(wait_page, self.participant.id))

        self.player.payoff = total_wait_page_pts
        self.player.save()

        return {'payoffs': self.get_payoffs()}
    
    pass


page_sequence = [
    Results
]
