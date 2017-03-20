from crispy_forms.helper import FormHelper
from allauth.account.forms import LoginForm, ChangePasswordForm, ResetPasswordForm, ResetPasswordKeyForm, \
    PasswordField, SetPasswordField, PasswordVerificationMixin
from django import forms
from django.utils.translation import ugettext_lazy as _


class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].label = 'E-mail'
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'


class ChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'


class ResetPasswordForm(ResetPasswordForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'


class ResetPasswordKeyForm(ResetPasswordKeyForm):
    def __init__(self, *args, **kwargs):
        super(ResetPasswordKeyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'


class AccountCreationForm(PasswordVerificationMixin, forms.Form):

    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)

    password1 = SetPasswordField(label=_("Set Password"))
    password2 = PasswordField(label=_("Password (again)"))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.temp_key = kwargs.pop("temp_key", None)
        self.session_key = kwargs.pop("sid", None)
        super(AccountCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].user = self.user
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.label_class = 'col-lg-4'
        self.helper.field_class = 'col-lg-6'

    def save(self):
        self.user.first_name = self.cleaned_data['first_name']
        self.user.last_name = self.cleaned_data['last_name']
        self.user.set_password(self.cleaned_data['password1'])
        self.user.is_active = True
        self.user.save()
        print(self.session_key)
