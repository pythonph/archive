# from django.views.generic.edit import FormMixin
from django.views.generic import FormView, DetailView, UpdateView
from django.contrib.auth.models import User

from braces.views import LoginRequiredMixin

from .models import UserProfile
from .forms import UserProfileForm


class GetProfileMixin(object):
    """ Generic profile mixin that knows how to fetch profile. """

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return UserProfile.objects.get(slug=slug)
        except Proposal.DoesNotExist:
            raise Http404
        

class ProfileDetailsView(GetProfileMixin, DetailView):
    template_name = 'profile/details.html'
    model = UserProfile
    context_object_name = 'profile'


class ProfileEditView(LoginRequiredMixin, GetProfileMixin, UpdateView):
    template_name = 'profile/edit.html'
    model = UserProfile
    form_class = UserProfileForm

    def get_initial(self):
        data = super(ProfileEditView, self).get_initial()

        # since first_name and last_name are coming from user,
        # attach it manually here to the form.
        profile = self.get_object()
        data['first_name'] = profile.user.first_name
        data['last_name'] = profile.user.last_name

        return data
