# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Person.supervisor'
        db.alter_column('main_person', 'supervisor_id', self.gf('mptt.fields.TreeForeignKey')(null=True, to=orm['main.Person']))


    def backwards(self, orm):
        
        # Changing field 'Person.supervisor'
        db.alter_column('main_person', 'supervisor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['main.Person']))


    models = {
        'main.person': {
            'Meta': {'object_name': 'Person'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'supervisor': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subordinate'", 'null': 'True', 'to': "orm['main.Person']"}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['main']
