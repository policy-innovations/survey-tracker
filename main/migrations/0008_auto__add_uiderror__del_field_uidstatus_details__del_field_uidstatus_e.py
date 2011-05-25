# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'UIDError'
        db.create_table('main_uiderror', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('etype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.ErrorType'])),
            ('uid_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.UIDStatus'])),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('main', ['UIDError'])

        # Deleting field 'UIDStatus.details'
        db.delete_column('main_uidstatus', 'details')

        # Deleting field 'UIDStatus.error'
        db.delete_column('main_uidstatus', 'error_id')


    def backwards(self, orm):
        
        # Deleting model 'UIDError'
        db.delete_table('main_uiderror')

        # Adding field 'UIDStatus.details'
        db.add_column('main_uidstatus', 'details', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)

        # Adding field 'UIDStatus.error'
        db.add_column('main_uidstatus', 'error', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['main.ErrorType'], blank=True), keep_default=False)


    models = {
        'main.errortype': {
            'Meta': {'object_name': 'ErrorType'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'suberrors'", 'null': 'True', 'to': "orm['main.ErrorType']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'main.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'main.role': {
            'Meta': {'object_name': 'Role'},
            'head': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subordinate'", 'null': 'True', 'to': "orm['main.Role']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Project']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'main.uiderror': {
            'Meta': {'object_name': 'UIDError'},
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'etype': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ErrorType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'uid_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.UIDStatus']"})
        },
        'main.uidstatus': {
            'Meta': {'object_name': 'UIDStatus'},
            'errors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['main.ErrorType']", 'null': 'True', 'through': "orm['main.UIDError']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Project']"}),
            'responsibles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Role']", 'symmetrical': 'False'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['main']
