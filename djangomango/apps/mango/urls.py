from django.conf.urls.defaults import patterns, url

from .views import HomeView, SubmitProposalView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^submit/$', SubmitProposalView.as_view(), name='submit_proposal'),
)
