from django.contrib.auth.decorators import login_required
from . import models
from ._builtin import Page, WaitPage


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class Introduction(Page):
    is_debug = False
    timeout_seconds = 60
    template_name = 'instructions_anagrams/Introduction.html'

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

class JoinTeamWaitPage(WaitPage):
    is_debug = False
    template_name = 'instructions_anagrams/JoinTeam.html'

    # This is fine... no method to run once all join.
    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

class TeamSummary(Page):
    is_debug = False
    timeout_seconds = 60
    template_name = 'instructions_anagrams/TeamSummary.html'

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

    def get_allowed_players(self):
        players = []
        for player in self.subsession.get_players():
            if player.participant.vars['consent'] and player.participant.vars['playing']:
                players.append(player)
        return players
        
    def vars_for_template(self):
        return {'N': len(self.get_allowed_players())}

class InstructionsPhase1(Page):
    is_debug = False
    timeout_seconds = 300    
    
    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing'] and \
                        'anagrams' in self.session.config['app_sequence']:
            return True
        else:
            return False

class InstructionsPhase1_Quiz(Page):
    required = True
    form_model = models.Player
    form_fields = ['anagram_hidden']
    is_debug = False
    timeout_seconds = 120

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
            self.participant.vars['anagrams_wait_required'] = True

class DifiIndexBefore(Page):
    is_debug = False
    required = True
    form_model = models.Player
    form_fields = ['distanceScale_before', 'overlapScale_before']

    timeout_seconds = 60
    
    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False
            self.participant.vars['anagrams_wait_required'] = True

page_sequence = [
    Introduction,
    JoinTeamWaitPage,
    TeamSummary,
    DifiIndexBefore,
    InstructionsPhase1,
    InstructionsPhase1_Quiz,
]
