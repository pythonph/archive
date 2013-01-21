from django.conf.urls.defaults import patterns, url

from .views import ProfileDetailsView


urlpatterns = patterns('',
    url(
        r'^(?P<slug>[-\w]+)/$',
        ProfileDetailsView.as_view(),
        name='profile_details'
    ),
)
