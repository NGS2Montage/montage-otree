from django.contrib.auth.decorators import login_required
from annoying.decorators import render_to
from .models import Game, GameStates
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.conf import settings


@render_to('state-mismatch.html')
@login_required
def state_mismatch(request):
    context = {
        "game": Game.objects.get_current_game()
    }
    # fill in context dict with stuff to pass to template as needed
    return context


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class MyRedirectView(LoginRequiredMixin, RedirectView):
    login_url = settings.LOGIN_URL

    def get(self, request, *args, **kwargs):
        user = request.user
        user_state = user.profile.state
        game_state = user.profile.game.state
        if user_state.state_code == 'pre':
            self.url = reverse(user_state.url_name)
        elif user_state in game_state.allowed_user_states.all():
            self.url = reverse(user_state.url_name)
        elif game_state == user_state:
            self.url = reverse(user_state.url_name)
        else:
            self.url = reverse('oops')

        return super(MyRedirectView, self).get(request, args, kwargs)
