from django import forms

from .models import Proposal


class SubmitProposalForm(forms.ModelForm):
    class Meta:
        model = Proposal
        fields = ('title', 'type', 'audience', 'category', 'duration',
                  'description', 'abstract')
