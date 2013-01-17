from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, FormView
from django.utils.translation import ugettext as _

from .forms import SubmitProposalForm
from ..proposal.models import Proposal


class HomeView(ListView):
    template_name = 'mango/approved_proposal_list.html'
    queryset = Proposal.objects.filter(status='approved')
    context_object_name = 'proposal_list'


class SubmitProposalView(FormView):
    template_name = 'mango/submit_proposal.html'
    form_class = SubmitProposalForm
