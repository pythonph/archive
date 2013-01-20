from django.contrib import messages
from django.views.generic import CreateView

from .forms import SubmitProposalForm
from .models import PENDING


class SubmitProposalView(CreateView):
    form_class = SubmitProposalForm
    template_name = 'mango/submit_proposal.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.speaker = self.request.user
        form.instance.status = PENDING
        return super(SubmitProposalView, self).form_valid(form)
