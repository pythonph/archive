# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models
from django.utils.translation import ugettext as _

from ..models import ProposalType, Category, AudienceLevel


PROPOSAL_TYPES = [_(u'Talk'), _(u'Tutorial'), _(u'Poster')]
CATEGORIES = [_(u'Best Practices/Patterns'), _(u'Big Data'), _(u'Business'),
    _(u'Cloud'), _(u'Community'), _(u'Concurrency'),
    _(u'Core Python (Language, Stdlib)'), _(u'Databases/NoSQL'),
    _(u'Distributed Computing'), _(u'Documentation'), _(u'Education'),
    _(u'Embedded Systems'), _(u'GUI Programming'), _(u'Gaming'),
    _(u'High Performance Computing'), _(u'Industry Uses'), _(u'Mobile'),
    _(u'Other'), _(u'Packaging'), _(u'Python Internals'), _(u'Science'),
    _(u'Systems Administration'), _(u'Testing'), _(u'Useful libraries'),
    _(u'Web Frameworks')]
AUDIENCE_LEVELS = [_(u'Novice'), _(u'Intermediate'), _(u'Experienced')]


class Migration(DataMigration):

    def forwards(self, orm):
        for type_name in PROPOSAL_TYPES:
            ProposalType.objects.create(name=type_name)

        for category in CATEGORIES:
            Category.objects.create(name=category)

        for audience_level in AUDIENCE_LEVELS:
            AudienceLevel.objects.create(name=audience_level)

    def backwards(self, orm):
        ProposalType.objects.filter(name__in=PROPOSAL_TYPES).delete()
        Category.objects.filter(name__in=CATEGORIES).delete()
        AudienceLevel.objects.filter(name__in=AUDIENCE_LEVELS).delete()

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proposal.audiencelevel': {
            'Meta': {'object_name': 'AudienceLevel'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proposal.category': {
            'Meta': {'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'proposal.proposal': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Proposal'},
            'abstract': ('django.db.models.fields.TextField', [], {}),
            'audience': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposal.AudienceLevel']"}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposal.Category']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'duration': ('django.db.models.fields.TimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('autoslug.fields.AutoSlugField', [], {'unique_with': '()', 'max_length': '50', 'populate_from': "'title'"}),
            'speaker': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'proposals'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'pending'", 'max_length': '10'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['proposal.ProposalType']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'})
        },
        'proposal.proposaltype': {
            'Meta': {'object_name': 'ProposalType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['proposal']
    symmetrical = True
