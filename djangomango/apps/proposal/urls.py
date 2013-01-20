from django.conf.urls.defaults import patterns, url

from .views import SubmitProposalView


urlpatterns = patterns('',
    url(r'^submit/$', SubmitProposalView.as_view(), name='submit_proposal'),
)
