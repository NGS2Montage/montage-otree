from . import models
from ._builtin import Page
from django.contrib.auth.decorators import login_required


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class Consent(LoginRequiredMixin, Page):
    form_model = models.Player
    form_fields = ['consent']
    is_debug = False


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


page_sequence = [
    Consent,
    ByeBye,
    Demographic
]
