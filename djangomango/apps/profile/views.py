# from django.views.generic.edit import FormMixin
from django.views.generic import FormView, DetailView
from django.contrib.auth.models import User

from .models import UserProfile
from .forms import ProfileForm


class ProfileDetailsView(DetailView):
    template_name = 'profile/details.html'
    model = UserProfile
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return UserProfile.objects.get(slug=slug)
        except Proposal.DoesNotExist:
            raise Http404
