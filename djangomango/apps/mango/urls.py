from django.conf.urls.defaults import patterns, url, include

from .views import HomeView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
)
