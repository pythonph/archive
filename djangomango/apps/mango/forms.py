from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User


class SignupForm(forms.Form):
    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        """ Make sure email is unique. """
        email = self.cleaned_data.get('email', None)
        try:
            User.objects.get(email=email)
            raise forms.ValidationError(_("Email already taken."))
        except User.DoesNotExist:
            return email

    def clean(self):
        """ Make sure password matches. """
        password = self.cleaned_data.get('password', None)
        confirm_password = self.cleaned_data.get('confirm_password', None)
        if password != confirm_password:
            self._errors['password'] = [_("Password doesn't match.")]
            self._errors['confirm_password'] = ' '  # highlight field
            raise forms.ValidationError('')
        return self.cleaned_data
