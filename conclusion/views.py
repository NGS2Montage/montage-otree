from otree.api import Currency as c, currency_range
from . import models
from ._builtin import Page, WaitPage
from .models import Constants

class Results(Page):
    
    is_debug = False
    timeout_seconds = 60
    
    def get_payoffs(self):
        to_display = {
            'anagrams': 'Anagrams Game', 
            'public_goods': 'Team Contribution Game', 
            'demographic_detailed': 'Optional Survey',
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
        
        return {'payoffs': self.get_payoffs()}
    
    pass


page_sequence = [
    Results
]
