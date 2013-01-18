from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, CreateView
from django.utils.translation import ugettext as _

from ..proposal.models import Proposal
from .forms import SubmitProposalForm


class HomeView(ListView):
    template_name = 'mango/approved_proposal_list.html'
    queryset = Proposal.objects.filter(status='approved')
    context_object_name = 'proposal_list'


class SubmitProposalView(CreateView):
    form_class = SubmitProposalForm
    template_name = 'mango/submit_proposal.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.speaker = self.request.user
        form.instance.status = 'pending'
        return super(SubmitProposalView, self).form_valid(form)
