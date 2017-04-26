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
    template_name = 'instructions/Introduction.html'

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False


class InstructionsPhase1(Page):
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
        question2_str = "__".join(self.request.POST.getlist('question2[]'))
        question3_str = "__".join(self.request.POST.getlist('question3[]'))
        question4_str = "__".join(self.request.POST.getlist('question4[]'))

        score = 0
        if question1_str == self.player.anagram_question1_solution:
            score += 1
        if question2_str == self.player.anagram_question2_solution:
            score += 1
        if question3_str == self.player.anagram_question3_solution:
            score += 1
        if question4_str == self.player.anagram_question4_solution:
            score += 1

        if score < 3:
            return "You got %d question(s) correct.\n" \
                   "You need to get at least 3 out of 4 questions correct.\n" \
                   "Please try again" % score
        else:
            self.player.anagram_question1 = question1_str
            self.player.anagram_question2 = question2_str
            self.player.anagram_question3 = question3_str
            self.player.anagram_question4 = question4_str
            self.player.anagram_score = score

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False



class InstructionsPhase2(Page):
    form_model = models.Player
    form_fields = ['public_goods_hidden']
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
            return "You need to get this question correct, before you could proceed." \
                   "Please try again"
        else:
            self.player.public_goods_question1 = question1_str
            self.player.public_goods_score = score

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False


class InstructionsPhase3(Page):
    form_model = models.Player
    form_fields = ['ultimatum_question1']
    is_debug = False

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                        'ultimatum' in self.session.config['app_sequence']:
            return True
        else:
            return False

    def error_message(self, values):
        question2_str = "__".join(self.request.POST.getlist('question2[]'))
        question3_str = "__".join(self.request.POST.getlist('question3[]'))
        question4_str = "__".join(self.request.POST.getlist('question4[]'))
        question5_str = "__".join(self.request.POST.getlist('question5[]'))

        score = 0
        if values['ultimatum_question1'] == self.player.ultimatum_question1_solution:
            score += 1
        if question2_str == self.player.ultimatum_question2_solution:
            score += 1
        if question3_str == self.player.ultimatum_question3_solution:
            score += 1
        if question4_str == self.player.ultimatum_question4_solution:
            score += 1
        if question5_str == self.player.ultimatum_question5_solution:
            score += 1

        if score < 4:
            return "You got %d question(s) correct.\n" \
                   "You need to get at least 4 out of 5 questions correct.\n" \
                   "Please try again" % score
        else:
            self.player.ultimatum_question2 = question2_str
            self.player.ultimatum_question3 = question3_str
            self.player.ultimatum_question4 = question4_str
            self.player.ultimatum_question5 = question5_str
            self.player.ultimatum_score = score

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False


page_sequence = [
    Introduction,
    InstructionsPhase1,
    InstructionsPhase2,
#    InstructionsPhase3
]
