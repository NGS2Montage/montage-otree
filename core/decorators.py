import logging
logger = logging.getLogger(__name__)

from django.conf import settings
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


'''
def game_state_required(user_state, game_state, *dec_args, **dec_kwargs):
    def _decorator(view_func):
        def _view(request, *args, **kwargs):
            if request.user.is_anonymous():
                return view_func(request, *args, **kwargs)

            current_game_state = request.user.profile.game.state.state_code
            current_user_state = request.user.profile.state.state_code

            if current_game_state == game_state and current_user_state == user_state:
                return view_func(request, *args, **kwargs)

            if current_game_state in dec_kwargs and current_user_state in dec_kwargs[current_game_state]:
                return HttpResponseRedirect(reverse(dec_kwargs[current_game_state][current_user_state]))

            if settings.DEBUG:
                from django.contrib import messages
                messages.add_message(request, messages.INFO, "State mismatched while requesting {}".format(request.path))
                messages.add_message(request, messages.INFO, "Required game state {}".format(game_state))
                messages.add_message(request, messages.INFO, "Required user state {}".format(user_state))

            return HttpResponseRedirect(reverse('redirect'))
        return _view
    return _decorator
'''
