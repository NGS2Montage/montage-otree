from . import models
from ._builtin import Page, WaitPage
from django.contrib.auth.decorators import login_required
import floppyforms.__future__ as forms


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

class SurveyConsent(Page):
    is_debug = False
    form_model = models.Player
    form_fields = ['participate']

    def is_displayed(self):
        if self.participant.vars['consent'] and\
            self.participant.vars['playing']:
            
            return True
        else:
            return False

class Demographic(Page):
    
    form_model = models.Player
    template_name = 'demographic_detailed/Demographic.html'
    form_fields = [
        "income", 
        "house", 
        "marital_status", 
        "friends",
        "country_born", 
        "country_reside", 
        "year_moved",
        "city_reside",
        "density",
        "ethnicity",
        "employment_status",
        "free_time",
        "specialty",
        "occupation",
    ]
    
    form_field_skip = ['{}_skip'.format(s) for s in form_fields]
    form_field_skip += [
        'age_residence_skip', 
        'activity_young_skip',
        'activity_old_skip',
        ]

    form_fields += ['age_residence_{}'.format(i) for i in [6,12,18,65,"Over65"]]
    form_fields += ['activity_young_{}'.format(i) for i in [
        'school',
        'afterSchool',
        'weekend',
        'sports',
        'flu',
        ]]
    form_fields += ['activity_old_{}'.format(i) for i in [
        'work',
        'school',
        'ptrans',
        'group',
        'sports',
        'flu',
        ]]

    form_fields += form_field_skip
    form_fields += ['nSkips']

    is_debug = False

    def is_displayed(self):
        if self.player.participate and\
           self.participant.vars['consent'] and\
           self.participant.vars['playing']:
            return True
        else:
            return False

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False
            self.player.payoff = 0
        else:
            if self.player.nSkips < 4:
                self.player.payoff = self.session.config['optional_survey_payout'] 
            else:
                self.player.payoff = 0

class Results(Page):

    def is_displayed(self):
        if self.participant.vars['consent'] and self.participant.vars['playing']:
            return True
        else:
            return False

    def vars_for_template(self):
        if self.player.participate:
            return {'nQuestions': 17 - self.player.nSkips}
    pass

page_sequence = [
    SurveyConsent,
    Demographic,
    Results
]
