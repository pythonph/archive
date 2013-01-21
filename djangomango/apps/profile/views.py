from django.contrib import messages
from django.views.generic import DetailView, UpdateView
from django.http import Http404
from django.utils.translation import ugettext as _

from braces.views import LoginRequiredMixin

from .models import UserProfile
from .forms import UserProfileForm


class GetProfileMixin(object):
    """ Generic profile mixin that knows how to fetch profile. """

    def get_object(self, queryset=None):
        slug = self.kwargs.get(self.slug_url_kwarg, None)
        try:
            return UserProfile.objects.get(slug=slug)
        except UserProfile.DoesNotExist:
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

    def form_valid(self, form):
        form.instance.user.first_name = form.cleaned_data['first_name']
        form.instance.user.last_name = form.cleaned_data['last_name']
        form.instance.user.save()
        messages.info(self.request, _(u"Your profile has been updated."))
        return super(ProfileEditView, self).form_valid(form)
