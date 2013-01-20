from django import forms
from django.contrib.admin import widgets
from django.utils.translation import ugettext_lazy as _

from .models import Proposal


class SubmitProposalForm(forms.ModelForm):
    duration = forms.CharField(widget=forms.TimeInput(
        attrs={'placeholder': '00:00'}))

    class Meta:
        model = Proposal
        fields = ('title', 'type', 'audience', 'category', 'duration',
                  'description', 'abstract')
