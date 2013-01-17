from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

from registration.forms import RegistrationFormUniqueEmail


class SignupForm(RegistrationFormUniqueEmail):
    """ Custom signup form that adds first_name and last_name fields. """

    first_name = forms.CharField()
    last_name = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        # delete username field and reorder first_name and last_name
        del self.fields['username']
        self.fields.insert(1, 'first_name', self.fields['first_name'])
        self.fields.insert(2, 'last_name', self.fields['last_name'])

    def clean_email(self):
        """ Error message is too long so we intercept and re-raise. """
        try:
            return super(SignupForm, self).clean_email()
        except forms.ValidationError:
            raise forms.ValidationError(
                _("This email address is already in use."))


class LoginForm(AuthenticationForm):
    """ Custom login form that override username as email. """

    username = forms.EmailField(label=_("Email"))
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username,
                                           password=password)

            if self.user_cache is None or not self.user_cache.is_active:
                self._errors['password'] = self._errors['username'] = ' '
                raise forms.ValidationError(
                    _("Its either your email or password is incorrect."))

        self.check_for_test_cookie()
        return self.cleaned_data
