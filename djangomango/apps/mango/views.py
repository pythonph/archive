from django.views.generic import TemplateView, ListView

from ..proposal.models import Proposal


class HomeView(ListView):
    queryset = Proposal.objects.filter(status='approved')
    context_object_name = 'proposal_list'
    template_name = 'mango/approved_proposal_list.html'
