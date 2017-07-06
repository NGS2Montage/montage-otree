from django.contrib.auth.decorators import login_required
from . import models
from ._builtin import Page, WaitPage
from .models import Constants


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class OpinionPage(Page):
    timeout_seconds = 60
    form_model = models.Player
    form_fields = [
        'ruse_Q1',
        'ruse_Q2',
        'ruse_Q3',
    ]
    is_debug = False

    def is_displayed(self):
        if self.participant.vars['consent'] and \
           self.participant.vars['playing']:

            return True
        else:
            return False
    
#    def before_next_page(self):
#        if self.timeout_happened:
#            self.participant.vars['playing'] = False

class Introduction(Page):
    is_debug = False
    timeout_seconds = 60
    
    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False
    
    pass

class WaitPage(WaitPage):
    is_debug = False
    title_text = "Processing Predictions"
    body_text = """Thank you, please wait while the rest of the team submits their
    predictions."""

    def is_displayed(self):
        if self.participant.vars['consent'] and \
           self.participant.vars['playing']:

            return True
        else:
            return False
 
class Results(Page):
    is_debug = False
    timeout_seconds = 60
    
    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

page_sequence = [
    Introduction,
    OpinionPage,
    WaitPage,
    Results,
]
