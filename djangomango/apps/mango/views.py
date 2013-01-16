from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.views.generic import TemplateView, ListView, FormView
from django.utils.translation import ugettext as _

from .forms import SignupForm
from ..proposal.models import Proposal


class HomeView(ListView):
    template_name = 'mango/approved_proposal_list.html'
    queryset = Proposal.objects.filter(status='approved')
    context_object_name = 'proposal_list'


class SignupView(FormView):
    template_name = 'mango/signup.html'
    form_class = SignupForm
    success_url = '/'

    def form_invalid(self, form):
        messages.error(self.request, _('Please fill-up the form properly.'))
        return super(SignupView, self).form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        password = form.cleaned_data['password']

        # create new user
        user = User.objects.create(username=email,
                                   email=email,
                                   first_name=first_name,
                                   last_name=last_name,
                                   is_active=True)
        user.set_password(password)
        user.save()

        # login new user automatically
        user = authenticate(username=email, password=password)
        if user: login(self.request, user)

        messages.info(self.request, _('Welcome %s!') % first_name)
        return super(SignupView, self).form_valid(form)
