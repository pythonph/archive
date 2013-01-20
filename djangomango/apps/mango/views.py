from django.views.generic import ListView

from ..proposal.models import Proposal, APPROVED


class HomeView(ListView):
    template_name = 'mango/approved_proposals.html'
    queryset = Proposal.objects.filter(status=APPROVED)
    context_object_name = 'proposal_list'
