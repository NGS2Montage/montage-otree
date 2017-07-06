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
    template_name = 'welcome/Introduction.html'


page_sequence = [
    Introduction,
]
