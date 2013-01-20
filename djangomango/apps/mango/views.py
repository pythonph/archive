from django.views.generic import ListView

from ..proposal.models import Proposal, APPROVED


class HomeView(ListView):
    template_name = 'mango/approved_proposal_list.html'
    queryset = Proposal.objects.filter(status=APPROVED)
    context_object_name = 'proposal_list'
