# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.contrib.auth.models import Group


class Migration(DataMigration):

    def forwards(self, orm):
        group = Group(name="moderator")
        group.save()

    def backwards(self, orm):
        try:
            Group.objects.get(name="moderator").delete()
        except Group.DoesNotExist:
            pass

    models = {
        
    }

    complete_apps = ['mango']
    symmetrical = True
