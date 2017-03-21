from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import FormView
from allauth.account.views import AjaxCapableProcessFormViewMixin, _ajax_response
from .forms import AccountCreationForm
from allauth.account.forms import UserTokenForm
from otree.models import Participant

from django.views.generic import TemplateView
from django.contrib.auth.models import User


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


class MyRedirectView(LoginRequiredMixin, RedirectView):
    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_staff:
            self.url = '/demo/'
            return super(MyRedirectView, self).get(request, args, kwargs)
        try:
            user_association = user.userparticipantassociation
        except Exception as e:
            self.url = reverse('no-association')
            return super(MyRedirectView, self).get(request, args, kwargs)

        if user_association.session is None:
            self.url = reverse('no-association')
            return super(MyRedirectView, self).get(request, args, kwargs)

        # if user_association.consent is False:
        #     self.url = reverse('no-consent')
        #     return super(MyRedirectView, self).get(request, args, kwargs)

        if user_association.participant is None:
            empty_participants = Participant.objects.filter(label__isnull=True,
                                                            session_id=user_association.session).order_by('id')
            if len(empty_participants) == 0:
                self.url = reverse('max-participants')
                return super(MyRedirectView, self).get(request, args, kwargs)
            user_association.participant = empty_participants[0]
            user_association.save()
            participant = user_association.participant
            participant.label = user.email
            participant.save()
            user_code = user_association.participant.code
            self.url = '/InitializeParticipant/%s/' % user_code
            return super(MyRedirectView, self).get(request, args, kwargs)
        else:
            user_code = user_association.participant.code
            self.url = '/InitializeParticipant/%s/' % user_code
            return super(MyRedirectView, self).get(request, args, kwargs)


class CreateAccountView(AjaxCapableProcessFormViewMixin, FormView):
    template_name = ("account/create_account_from_key.html")
    form_class = AccountCreationForm
    success_url = reverse_lazy("account_created")

    def dispatch(self, request, uid, key, sid, **kwargs):
        self.request = request
        self.key = key
        self.sid = sid

        token_form = UserTokenForm(data={'uidb36': uid, 'key': key})

        if not token_form.is_valid():
            self.reset_user = None
            response = self.render_to_response(
                self.get_context_data(token_fail=True)
            )
            return _ajax_response(self.request, response, form=token_form)
        else:
            self.reset_user = token_form.reset_user
            return super(CreateAccountView, self).dispatch(request, uid, key, sid, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(CreateAccountView, self).get_form_kwargs()
        kwargs["user"] = self.reset_user
        kwargs["temp_key"] = self.key
        kwargs['sid'] = self.sid
        return kwargs

    def get_context_data(self, **kwargs):
        ret = super(CreateAccountView, self).get_context_data(**kwargs)
        ret['email'] = self.reset_user
        return ret

    def form_valid(self, form):
        form.save()
        return super(CreateAccountView, self).form_valid(form)


create_account = CreateAccountView.as_view()


class AdditionUserView(TemplateView):
    def get(self, request, *args, **kwargs):
        u = User.objects.get(email='parang2@vt.edu')
        u.first_name = 'Parang'
        u.last_name = 'Saraf'
        u.set_password('temp12')
        u.save()
        return super(AdditionUserView, self).get(request, args, kwargs)
