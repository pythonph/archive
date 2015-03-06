# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.conf import settings
from django.contrib.sites.models import Site


class Migration(DataMigration):

    def forwards(self, orm):
        try:
            site = Site.objects.all()[0]
            site.name = settings.SITE_NAME
            site.domain = settings.SITE_HOSTNAME
            site.save()
        except IndexError:
            pass

    def backwards(self, orm):
        try:
            site = Site.objects.all()[0]
            site.name = 'example.com'
            site.domain = 'example.com'
            site.save()
        except IndexError:
            pass

    models = {
        
    }

    complete_apps = ['mango']
    symmetrical = True
