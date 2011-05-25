# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Error'
        db.delete_table('main_error')

        # Adding model 'ErrorType'
        db.create_table('main_errortype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='suberrors', null=True, to=orm['main.ErrorType'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('main', ['ErrorType'])

        # Adding field 'UIDStatus.error'
        db.add_column('main_uidstatus', 'error', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['main.ErrorType'], blank=True), keep_default=False)

        # Adding field 'UIDStatus.details'
        db.add_column('main_uidstatus', 'details', self.gf('django.db.models.fields.TextField')(default='', blank=True), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Error'
        db.create_table('main_error', (
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('details', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(related_name='suberrors', null=True, to=orm['main.Error'], blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Error'])

        # Deleting model 'ErrorType'
        db.delete_table('main_errortype')

        # Deleting field 'UIDStatus.error'
        db.delete_column('main_uidstatus', 'error_id')

        # Deleting field 'UIDStatus.details'
        db.delete_column('main_uidstatus', 'details')


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
        'main.uidstatus': {
            'Meta': {'object_name': 'UIDStatus'},
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'error': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.ErrorType']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Project']"}),
            'responsibles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Role']", 'symmetrical': 'False'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['main']
