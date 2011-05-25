# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'IdStatus'
        db.create_table('main_idstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('uid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('main', ['IdStatus'])

        # Adding M2M table for field responsibles on 'IdStatus'
        db.create_table('main_idstatus_responsibles', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('idstatus', models.ForeignKey(orm['main.idstatus'], null=False)),
            ('person', models.ForeignKey(orm['main.person'], null=False))
        ))
        db.create_unique('main_idstatus_responsibles', ['idstatus_id', 'person_id'])

        # Deleting field 'Person.supervisor'
        db.delete_column('main_person', 'supervisor_id')

        # Adding field 'Person.head'
        db.add_column('main_person', 'head', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='subordinate', null=True, to=orm['main.Person']), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'IdStatus'
        db.delete_table('main_idstatus')

        # Removing M2M table for field responsibles on 'IdStatus'
        db.delete_table('main_idstatus_responsibles')

        # Adding field 'Person.supervisor'
        db.add_column('main_person', 'supervisor', self.gf('mptt.fields.TreeForeignKey')(related_name='subordinate', null=True, to=orm['main.Person'], blank=True), keep_default=False)

        # Deleting field 'Person.head'
        db.delete_column('main_person', 'head_id')


    models = {
        'main.idstatus': {
            'Meta': {'object_name': 'IdStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'responsibles': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['main.Person']", 'symmetrical': 'False'}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'main.person': {
            'Meta': {'object_name': 'Person'},
            'head': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subordinate'", 'null': 'True', 'to': "orm['main.Person']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        }
    }

    complete_apps = ['main']
