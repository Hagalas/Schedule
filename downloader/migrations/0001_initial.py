# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FileCategory'
        db.create_table(u'downloader_filecategory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('code_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'downloader', ['FileCategory'])

        # Adding model 'File'
        db.create_table(u'downloader_file', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file_url', self.gf('django.db.models.fields.URLField')(default='http://wimii.pcz.pl/download/plan_stacjonarny/Plan_dzienne_lato_13_14_3_nauczyciel.html', max_length=200)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('addition_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['downloader.FileCategory'], null=True, blank=True)),
        ))
        db.send_create_signal(u'downloader', ['File'])


    def backwards(self, orm):
        # Deleting model 'FileCategory'
        db.delete_table(u'downloader_filecategory')

        # Deleting model 'File'
        db.delete_table(u'downloader_file')


    models = {
        u'downloader.file': {
            'Meta': {'object_name': 'File'},
            'addition_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['downloader.FileCategory']", 'null': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file_url': ('django.db.models.fields.URLField', [], {'default': "'http://wimii.pcz.pl/download/plan_stacjonarny/Plan_dzienne_lato_13_14_3_nauczyciel.html'", 'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'downloader.filecategory': {
            'Meta': {'object_name': 'FileCategory'},
            'code_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['downloader']