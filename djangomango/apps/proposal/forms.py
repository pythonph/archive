from django import forms

from .models import Proposal


class SubmitProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        exclude = ('speaker', 'status',)
