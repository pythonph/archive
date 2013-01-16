from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import logout

from .views import HomeView, SignupView


urlpatterns = patterns('',
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^signup/$', SignupView.as_view(), name='signup'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
)
