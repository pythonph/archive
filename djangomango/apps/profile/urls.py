from django.conf.urls.defaults import patterns, url

from .views import ProfileDetailsView, ProfileEditView


urlpatterns = patterns('',
    url(
        r'^(?P<slug>[-\w]+)/$',
        ProfileDetailsView.as_view(),
        name='profile_details'
    ),
    url(
        r'^edit/(?P<slug>[-\w]+)/$',
        ProfileEditView.as_view(),
        name='profile_edit'
    ),
)
