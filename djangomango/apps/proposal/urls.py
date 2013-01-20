from django.conf.urls.defaults import patterns, url

from .views import SubmitProposalView, ScheduleProposalView


urlpatterns = patterns('',
    url(r'^submit/$', SubmitProposalView.as_view(), name='submit_proposal'),
    url(r'^schedule/$', ScheduleProposalView.as_view(), name='schedule_proposal'),
)
