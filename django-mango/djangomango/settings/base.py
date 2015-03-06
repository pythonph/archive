"""Base settings shared by all environments"""
# Import global settings to make it easier to extend settings.
from django.conf.global_settings import *   # pylint: disable=W0614,W0401

#==============================================================================
# Generic Django project settings
#==============================================================================

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SITE_ID = 1
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
TIME_ZONE = 'Asia/Manila'
USE_TZ = True
USE_I18N = True
USE_L10N = True
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', 'English'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+7^r4ytsx9h2_@*2yl=(+9ub02l6w3(x8upx+lbll%%-kqq181'

INSTALLED_APPS = (
    'djangomango.apps.mango',
    'djangomango.apps.profile',
    'djangomango.apps.proposal',

    'south',
    'django_nose',
    'endless_pagination',
    'registration',
    'longerusername',
    'templatetag_handlebars',
    'imagekit',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
)

#==============================================================================
# Calculation of directories relative to the project module location
#==============================================================================

import os
import sys
import djangomango as project_module

PROJECT_DIR = os.path.dirname(os.path.realpath(project_module.__file__))

PYTHON_BIN = os.path.dirname(sys.executable)
ve_path = os.path.dirname(os.path.dirname(os.path.dirname(PROJECT_DIR)))
# Assume that the presence of 'activate_this.py' in the python bin/
# directory means that we're running in a virtual environment.
if os.path.exists(os.path.join(PYTHON_BIN, 'activate_this.py')):
    # We're running with a virtualenv python executable.
    VAR_ROOT = os.path.join(os.path.dirname(PYTHON_BIN), 'var')
elif ve_path and os.path.exists(os.path.join(ve_path, 'bin',
        'activate_this.py')):
    # We're running in [virtualenv_root]/src/[project_name].
    VAR_ROOT = os.path.join(ve_path, 'var')
else:
    # Set the variable root to a path in the project which is
    # ignored by the repository.
    VAR_ROOT = os.path.join(PROJECT_DIR, 'var')

if not os.path.exists(VAR_ROOT):
    os.mkdir(VAR_ROOT)

#==============================================================================
# Project URLS and media settings
#==============================================================================

ROOT_URLCONF = 'djangomango.urls'

LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'
LOGIN_REDIRECT_URL = '/'

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATIC_ROOT = os.path.join(VAR_ROOT, 'static')
MEDIA_ROOT = os.path.join(VAR_ROOT, 'uploads')

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
    os.path.join(PROJECT_DIR, 'uploads'),
)

#==============================================================================
# Templates
#==============================================================================

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'templates'),
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

#==============================================================================
# Middleware
#==============================================================================

MIDDLEWARE_CLASSES += (
)

#==============================================================================
# Auth / security
#==============================================================================

AUTHENTICATION_BACKENDS += (
    'djangomango.apps.mango.backends.EmailAuthBackend',
)

#==============================================================================
# Logging
#==============================================================================

LOGGING['formatters'] = {
    'simple': {
        'format': '[%(name)s] %(levelname)s %(asctime)s: %(message)s'
    }
}

LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'formatter': 'simple'
}

LOGGING['loggers']['generic'] = {
    'handlers': ['console'],
    'level': 'DEBUG'
}

#==============================================================================
# Email settings
#==============================================================================

EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = ''

#==============================================================================
# Miscellaneous project settings
#==============================================================================

AUTH_PROFILE_MODULE = 'mango.UserProfile'

# site info
SITE_NAME = 'PyCon Philippines'
SITE_HOSTNAME = ''

# SCSS
SCSS_LOAD_PATHS = [
    os.path.join(PROJECT_DIR, 'static', 'css/sass')
]

SCSS_OPTIONS = {
    'compress': True,
    'debug_info': True
}

SCSS_REBUILD = False

# coffeescript
COFFEE_REBUILD = False

# gravatar
GRAVATAR_URL = 'http://www.gravatar.com/avatar/'

#==============================================================================
# Third party app settings
#==============================================================================

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

ENDLESS_PAGINATION_PER_PAGE = 5
ENDLESS_PAGINATION_PREVIOUS_LABEL = '&laquo;'
ENDLESS_PAGINATION_NEXT_LABEL = '&raquo;'
