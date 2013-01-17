from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import logout

from .views import HomeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
)
