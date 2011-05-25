# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'IdStatus'
        db.delete_table('main_idstatus')

        # Removing M2M table for field responsibles on 'IdStatus'
        db.delete_table('main_idstatus_responsibles')

        # Deleting model 'Person'
        db.delete_table('main_person')

        # Adding model 'Project'
        db.create_table('main_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Project'])

        # Adding model 'Error'
        db.create_table('main_error', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='suberrors', null=True, to=orm['main.Error'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('main', ['Error'])

        # Adding model 'Role'
        db.create_table('main_role', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('head', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='subordinate', null=True, to=orm['main.Role'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Project'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('main', ['Role'])

        # Adding model 'UIDStatus'
        db.create_table('main_uidstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['main.Project'])),
        ))
        db.send_create_signal('main', ['UIDStatus'])

        # Adding M2M table for field responsibles on 'UIDStatus'
        db.create_table('main_uidstatus_responsibles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('uidstatus', models.ForeignKey(orm['main.uidstatus'], null=False)),
            ('role', models.ForeignKey(orm['main.role'], null=False))
        ))
        db.create_unique('main_uidstatus_responsibles', ['uidstatus_id', 'role_id'])


    def backwards(self, orm):
        
        # Adding model 'IdStatus'
        db.create_table('main_idstatus', (
            ('uid', self.gf('django.db.models.fields.CharField')(max_length=30, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['IdStatus'])

        # Adding M2M table for field responsibles on 'IdStatus'
        db.create_table('main_idstatus_responsibles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idstatus', models.ForeignKey(orm['main.idstatus'], null=False)),
            ('person', models.ForeignKey(orm['main.person'], null=False))
        ))
        db.create_unique('main_idstatus_responsibles', ['idstatus_id', 'person_id'])

        # Adding model 'Person'
        db.create_table('main_person', (
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('head', self.gf('mptt.fields.TreeForeignKey')(related_name='subordinate', null=True, to=orm['main.Person'], blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('main', ['Person'])

        # Deleting model 'Project'
        db.delete_table('main_project')

        # Deleting model 'Error'
        db.delete_table('main_error')

        # Deleting model 'Role'
        db.delete_table('main_role')

        # Deleting model 'UIDStatus'
        db.delete_table('main_uidstatus')

        # Removing M2M table for field responsibles on 'UIDStatus'
        db.delete_table('main_uidstatus_responsibles')


    models = {
        'main.error': {
            'Meta': {'object_name': 'Error'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'suberrors'", 'null': 'True', 'to': "orm['main.Error']"}),
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Project']"}),
            'responsibles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Role']", 'symmetrical': 'False'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['main']
