from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import login, logout
from django.contrib.auth.views import (password_reset, password_reset_confirm,
                                       password_reset_done,
                                       password_reset_complete)

from djangomango.apps.mango.forms import SignupForm, LoginForm

from registration.views import register


admin.site.login_form = LoginForm
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('djangomango.apps.mango.urls')),
    (r'^profile/', include('djangomango.apps.profile.urls')),
    (r'^proposal/', include('djangomango.apps.proposal.urls')),

    # contrib apps
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^login/$', login, {'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),
    url(
        r'^accounts/password/reset/$',
        password_reset,
        name='password_reset'
    ),
    url(
        r'^accounts/password/reset/done/$',
        password_reset_done,
        name='password_reset_done'
    ),
    url(
        r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        name='password_reset_confirm'
    ),
    url(
        r'^accounts/password/reset/complete/$',
        password_reset_complete,
        name='password_reset_complete'
    ),

    # 3rd party apps
    url(
        r'^signup/$',
        register,
        {
            'backend': 'djangomango.apps.mango.backends.RegistrationBackend',
            'template_name': 'registration/signup.html',
            'success_url': '/',
            'form_class': SignupForm
        },
        name='signup'
    ),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)