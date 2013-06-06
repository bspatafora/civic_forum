# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Posting'
        db.create_table(u'postings_posting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('variety', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal(u'postings', ['Posting'])

        # Adding model 'Comment'
        db.create_table(u'postings_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('posting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postings.Posting'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('user', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'postings', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Posting'
        db.delete_table(u'postings_posting')

        # Deleting model 'Comment'
        db.delete_table(u'postings_comment')


    models = {
        u'postings.comment': {
            'Meta': {'ordering': "['-points']", 'object_name': 'Comment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'posting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['postings.Posting']"}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'postings.posting': {
            'Meta': {'ordering': "['-points']", 'object_name': 'Posting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'variety': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        }
    }

    complete_apps = ['postings']