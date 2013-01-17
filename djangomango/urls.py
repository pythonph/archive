from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.conf.urls.defaults import patterns, url, include
from django.contrib.auth.views import login, logout
# from django.core.urlresolvers import reverse

from djangomango.apps.mango.forms import SignupForm, LoginForm

from registration.views import register


admin.site.login_form = LoginForm
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include('djangomango.apps.mango.urls')),

    # contrib apps
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),

    url(r'^login/$', login, {'authentication_form': LoginForm}, name='login'),
    url(r'^logout/$', logout, {'next_page': '/'}, name='logout'),

    # 3rd party apps
    url(r'^signup/$', register,
        {'backend': 'djangomango.apps.mango.backends.RegistrationBackend',
         'template_name': 'registration/signup.html',
         'success_url': '/',
         'form_class': SignupForm},
        name='signup'),
)

if settings.DEBUG and settings.MEDIA_ROOT:
    urlpatterns += static(settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT)