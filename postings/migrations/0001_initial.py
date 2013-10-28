# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Alert'
        db.create_table(u'postings_alert', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'postings', ['Alert'])

        # Adding model 'Posting'
        db.create_table(u'postings_posting', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=140)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('variety', self.gf('django.db.models.fields.CharField')(default='community', max_length=2)),
        ))
        db.send_create_signal(u'postings', ['Posting'])

        # Adding model 'Vote'
        db.create_table(u'postings_vote', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('access_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postings.Posting'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('more_like_this', self.gf('django.db.models.fields.CharField')(default='', max_length=2)),
        ))
        db.send_create_signal(u'postings', ['Vote'])

        # Adding model 'AlertComment'
        db.create_table(u'postings_alertcomment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('alert', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postings.Alert'])),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['postings.AlertComment'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=1)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'postings', ['AlertComment'])

        # Adding model 'Comment'
        db.create_table(u'postings_comment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('posting', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['postings.Posting'])),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['postings.Comment'])),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=10000)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('posted', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=1)),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'postings', ['Comment'])


    def backwards(self, orm):
        # Deleting model 'Alert'
        db.delete_table(u'postings_alert')

        # Deleting model 'Posting'
        db.delete_table(u'postings_posting')

        # Deleting model 'Vote'
        db.delete_table(u'postings_vote')

        # Deleting model 'AlertComment'
        db.delete_table(u'postings_alertcomment')

        # Deleting model 'Comment'
        db.delete_table(u'postings_comment')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'postings.alert': {
            'Meta': {'ordering': "['-updated']", 'object_name': 'Alert'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'postings.alertcomment': {
            'Meta': {'object_name': 'AlertComment'},
            'alert': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['postings.Alert']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['postings.AlertComment']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'postings.comment': {
            'Meta': {'object_name': 'Comment'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['postings.Comment']"}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'posting': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['postings.Posting']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'postings.posting': {
            'Meta': {'ordering': "['-posted']", 'object_name': 'Posting'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '10000'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'variety': ('django.db.models.fields.CharField', [], {'default': "'community'", 'max_length': '2'})
        },
        u'postings.vote': {
            'Meta': {'object_name': 'Vote'},
            'access_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['postings.Posting']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'more_like_this': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'posted': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['postings']