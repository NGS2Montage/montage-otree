from django.contrib.auth.decorators import login_required
from . import models
from ._builtin import Page


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class Introduction(Page):
    is_debug = False
    timeout_seconds = 60
    template_name = 'instructions_pgg/Introduction.html'

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

class InstructionsPhase2(Page):
    is_debug = False
    timeout_seconds = 60
    
    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                        'public_goods' in self.session.config['app_sequence']:
            return True
        else:
            return False

    def vars_for_template(self):
        return {'n_players': len(self.player.get_others_in_group()) + 1 }

class InstructionsPhase2_Quiz(Page):
    form_model = models.Player
    form_fields = ['public_goods_hidden']
    required = True
    timeout_seconds = 120
    
    is_debug = False

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                        'public_goods' in self.session.config['app_sequence']:
            return True
        else:
            return False

    def error_message(self, values):
        question1_str = "__".join(self.request.POST.getlist('question1[]'))

        score = 0
        if question1_str == self.player.public_goods_question1_solution:
            score += 1

        if score < 1:
            return "You need to get this question correct, before you can proceed." \
                   "Please try again"
        else:
            self.player.public_goods_question1 = question1_str
            self.player.public_goods_score = score

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False
            self.participant.vars['pgg_arrival_wait'] = True



page_sequence = [
    Introduction,
    InstructionsPhase2,
    InstructionsPhase2_Quiz,
]
