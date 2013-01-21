from django.views.generic import ListView, TemplateView

from ..proposal.models import Proposal, APPROVED


class HomeView(TemplateView):
    template_name = 'mango/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # add approved proposals
        context['proposal_list'] = Proposal.objects.filter(status=APPROVED)

        # TODO: add speakers list
        context['speaker_list'] = None

        return context
