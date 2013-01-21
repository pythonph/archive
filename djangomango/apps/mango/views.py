from django.contrib.auth.models import User
from django.views.generic import TemplateView

from ..proposal.models import Proposal, APPROVED


class HomeView(TemplateView):
    template_name = 'mango/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # add approved proposals
        proposals = context['proposal_list'] = (Proposal.objects
                                                .filter(status=APPROVED))

        # add speakers list
        speaker_ids = proposals.distinct().values_list('speaker_id', flat=True)
        context['speaker_list'] = User.objects.filter(id__in=speaker_ids)

        return context
