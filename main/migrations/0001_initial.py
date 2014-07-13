# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DayTime'
        db.create_table(u'main_daytime', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('day', self.gf('django.db.models.fields.IntegerField')()),
            ('hour', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'main', ['DayTime'])

        # Adding model 'Subject'
        db.create_table(u'main_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('ects', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exam', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Subject'])

        # Adding model 'Group'
        db.create_table(u'main_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_nr', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('semester', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('field_of_study', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('degree', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('specialization', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Group'])

        # Adding model 'Faculty'
        db.create_table(u'main_faculty', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Faculty'])

        # Adding model 'Room'
        db.create_table(u'main_room', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('room_number', self.gf('django.db.models.fields.CharField')(default='0', max_length=5, null=True, blank=True)),
            ('faculty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Faculty'])),
        ))
        db.send_create_signal(u'main', ['Room'])

        # Adding model 'Teacher'
        db.create_table(u'main_teacher', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('surname', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('degree', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Room'], null=True, blank=True)),
            ('faculty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Faculty'])),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=45, null=True, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=12, null=True, blank=True)),
        ))
        db.send_create_signal(u'main', ['Teacher'])

        # Adding model 'Consultations'
        db.create_table(u'main_consultations', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Teacher'])),
            ('hour', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DayTime'])),
            ('faculty', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Faculty'])),
        ))
        db.send_create_signal(u'main', ['Consultations'])

        # Adding model 'Schedule'
        db.create_table(u'main_schedule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Subject'])),
            ('day_time', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.DayTime'])),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Group'])),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Teacher'])),
            ('room', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Room'])),
        ))
        db.send_create_signal(u'main', ['Schedule'])


    def backwards(self, orm):
        # Deleting model 'DayTime'
        db.delete_table(u'main_daytime')

        # Deleting model 'Subject'
        db.delete_table(u'main_subject')

        # Deleting model 'Group'
        db.delete_table(u'main_group')

        # Deleting model 'Faculty'
        db.delete_table(u'main_faculty')

        # Deleting model 'Room'
        db.delete_table(u'main_room')

        # Deleting model 'Teacher'
        db.delete_table(u'main_teacher')

        # Deleting model 'Consultations'
        db.delete_table(u'main_consultations')

        # Deleting model 'Schedule'
        db.delete_table(u'main_schedule')


    models = {
        u'main.consultations': {
            'Meta': {'object_name': 'Consultations'},
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Faculty']"}),
            'hour': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.DayTime']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Teacher']"})
        },
        u'main.daytime': {
            'Meta': {'object_name': 'DayTime'},
            'day': ('django.db.models.fields.IntegerField', [], {}),
            'hour': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'main.faculty': {
            'Meta': {'object_name': 'Faculty'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'})
        },
        u'main.group': {
            'Meta': {'object_name': 'Group'},
            'degree': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'field_of_study': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'group_nr': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'semester': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'specialization': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'main.room': {
            'Meta': {'object_name': 'Room'},
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Faculty']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room_number': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        u'main.schedule': {
            'Meta': {'object_name': 'Schedule'},
            'day_time': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.DayTime']"}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Room']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Subject']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Teacher']"})
        },
        u'main.subject': {
            'Meta': {'object_name': 'Subject'},
            'ects': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exam': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'main.teacher': {
            'Meta': {'object_name': 'Teacher'},
            'degree': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'faculty': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Faculty']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'room': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['main.Room']", 'null': 'True', 'blank': 'True'}),
            'surname': ('django.db.models.fields.CharField', [], {'max_length': '45'})
        }
    }

    complete_apps = ['main']