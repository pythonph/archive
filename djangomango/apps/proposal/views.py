from django.contrib import messages
from django.views.generic import CreateView, TemplateView
from django.utils.translation import ugettext as _
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import user_passes_test

from .forms import SubmitProposalForm
from .models import PENDING
from ..mango.utils import moderator_required


class SubmitProposalView(CreateView):
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
