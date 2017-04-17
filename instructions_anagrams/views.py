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
    template_name = 'instructions_anagrams/Introduction.html'

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

class InstructionsPhase1(Page):
    is_debug = False

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                        'anagrams' in self.session.config['app_sequence']:
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False



    pass

class InstructionsPhase1_Quiz(Page):
    form_model = models.Player
    form_fields = ['anagram_hidden']
    is_debug = False

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                        'anagrams' in self.session.config['app_sequence']:
            return True
        else:
            return False

    def error_message(self, values):
        question1_str = "__".join(self.request.POST.getlist('question1[]'))

        score = 0
        if question1_str == self.player.anagram_question1_solution:
            score += 1

        response = ""

        if ('b' in question1_str) or ('c' in question1_str):
            response += """Incorrect: Remember, the letter 'A' has not been approved by a
            teammate yet. You can only use the blue or green letters to form
            words. """

        if ('e' in question1_str):
            response += """\nIncorrect: Remember, words must have more than 2
            letters. """

        if score < 1:
            return response + """Please try again."""
        else:
            self.player.anagram_question1 = question1_str
            self.player.anagram_score = score

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False

page_sequence = [
    Introduction,
    InstructionsPhase1,
    InstructionsPhase1_Quiz,
]
