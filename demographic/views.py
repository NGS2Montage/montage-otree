from . import models
from ._builtin import Page
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class Consent(LoginRequiredMixin, Page):
    form_model = models.Player
    form_fields = ['consent']
    is_debug = False
    timeout_submission = {'consent': False}

    def before_next_page(self):
        user_participant = self.request.user.userparticipantassociation

        if self.player.consent is False:
            user_participant.consent = False
            user_participant.participant = None
            user_participant.save()
            self.participant.vars['consent'] = False
        else:
            user_participant.consent = True
            user_participant.save()


class ByeBye(LoginRequiredMixin, Page):
    is_debug = False

    def is_displayed(self):
        if self.player.consent:
            return False
        else:
            return True


class Demographic(LoginRequiredMixin, Page):
    form_model = models.Player
    form_fields = ["age", "income", "sex", "marital_status", "country_born", "country_reside", "year_moved",
                   "highest_degree", "speciality", "employment_status", "occupation", "religious_preference",
                   "other_religion", "device_type", "membership_duration", "access_turk", "access_turk_other",
                   "timezone", "timezone_access", "time_of_day", "hours_spent", "start_frequency", "location",
                   "location_other", "multitask", "multitask_yes", "hits", "number_of_studies", "participation_number"]
    is_debug = False
    timeout_submission = {"age": 1, "income": "Less than $25,000", "sex": "Male", "marital_status": "single",
                          "country_born": "Empty", "country_reside": "Empty", "year_moved": "0000",
                          "highest_degree": "Not Sure", "speciality": "None", "employment_status": "Unable to work",
                          "occupation": "None", "religious_preference": "Other", "other_religion": "None",
                          "device_type": "None", "membership_duration": "0", "access_turk": "Other",
                          "access_turk_other": "None", "timezone": "None", "timezone_access": "None",
                          "time_of_day": "4am-8am; early morning", "hours_spent": "0", "start_frequency": "Weekly",
                          "location": "Other", "location_other": "None", "multitask": "Yes", "multitask_yes": "None",
                          "hits": "None", "number_of_studies": 0, "participation_number": 0}

    def is_displayed(self):
        if self.player.consent:
            return True
        else:
            return False

    def error_message(self, values):
        err_messages = []
        if values['country_born'].strip() != values['country_reside'].strip():
            if values['year_moved'].strip() == "":
                err =  "You country of birth is different from your country of residence. However, you haven't filled" \
                       " the year you moved to your current country of residence in question 7."
                err_messages.append(err)

        if values['religious_preference'] == "Other" and values['other_religion'].strip() == "":
            err = "In question 12, you selected religion as other, however you haven't filled the other religion in " \
                  "question 13."
            err_messages.append(err)

        if values['access_turk'] == "Other" and values['access_turk_other'].strip() == "":
            err = "In question 16, you selected Other, however you haven't specified 'Other' in question 17."
            err_messages.append(err)

        if values['location'] == "Other" and values['location_other'].strip() == "":
            err = "In question 23 you selected Other, however you haven't specified 'Other' in question 24."
            err_messages.append(err)

        if values['multitask'] == "Yes" and values['multitask_yes'].strip() == "":
            err = "In question 25 you specified that you multitask, however you haven't specified what kind of other " \
                  "activity is involved while multitasking in question 26"
            err_messages.append(err)

        if len(err_messages) == 1:
            return err_messages[0]
        if len(err_messages) > 1:
            err_string = err_messages[0]
            for err in err_messages[1:]:
                err_string += "<li>"+err+"</li>"
            return err_string

    def before_next_page(self):
        if self.timeout_happened:
            self.participant.vars['playing'] = False


page_sequence = [
    Consent,
    ByeBye,
    Demographic
]
