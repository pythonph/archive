from django.contrib import messages
from django.views.generic import CreateView, TemplateView, DetailView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test
from django.http import Http404

from braces.views import LoginRequiredMixin

from .forms import SubmitProposalForm
from .models import APPROVED, PENDING, Proposal
from ..mango.utils import moderator_required


class ProposalDetailsView(DetailView):
    template_name = 'proposal/details.html'
    model = Proposal
    context_object_name = 'proposal'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return Proposal.objects.get(slug=slug, status=APPROVED)
        except Proposal.DoesNotExist:
            raise Http404


class SubmitProposalView(LoginRequiredMixin, CreateView):
    form_class = SubmitProposalForm
    template_name = 'proposal/submit.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.speaker = self.request.user
        form.instance.status = PENDING
        messages.info(self.request,
            _(u"Thank you, your proposal is now being reviewed."))
        return super(SubmitProposalView, self).form_valid(form)


class ScheduleProposalView(TemplateView):
    template_name = 'proposal/schedule.html'

    @method_decorator(user_passes_test(moderator_required))
    def dispatch(self, *args, **kwargs):
        return super(ScheduleProposalView, self).dispatch(*args, **kwargs)
