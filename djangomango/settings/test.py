"""
This settings is purely for testing purposes, ie. Travis.
"""

from djangomango.settings.base import *   # pylint: disable=W0614,W0401

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'djangomango.db'
    }
}
