# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'Project'
        db.delete_table('main_project')

        # Removing M2M table for field users on 'Project'
        db.delete_table('main_project_users')

        # Removing M2M table for field error_types on 'Project'
        db.delete_table('main_project_error_types')

        # Adding model 'Questionnaire'
        db.create_table('main_questionnaire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('hierarchy', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='questionnaire', unique=True, null=True, to=orm['main.Role'])),
        ))
        db.send_create_signal('main', ['Questionnaire'])

        # Adding M2M table for field users on 'Questionnaire'
        db.create_table('main_questionnaire_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionnaire', models.ForeignKey(orm['main.questionnaire'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('main_questionnaire_users', ['questionnaire_id', 'user_id'])

        # Adding M2M table for field error_types on 'Questionnaire'
        db.create_table('main_questionnaire_error_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionnaire', models.ForeignKey(orm['main.questionnaire'], null=False)),
            ('errortype', models.ForeignKey(orm['main.errortype'], null=False))
        ))
        db.create_unique('main_questionnaire_error_types', ['questionnaire_id', 'errortype_id'])

        # Adding model 'ConfirmationQuestion'
        db.create_table('main_confirmationquestion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='subquestions', null=True, to=orm['main.ConfirmationQuestion'])),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('main', ['ConfirmationQuestion'])

        # Deleting field 'UIDStatus.project'
        db.delete_column('main_uidstatus', 'project_id')

        # Adding field 'UIDStatus.questionnaire'
        db.add_column('main_uidstatus', 'questionnaire', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['main.Questionnaire']), keep_default=False)


    def backwards(self, orm):
        
        # Adding model 'Project'
        db.create_table('main_project', (
            ('hierarchy', self.gf('django.db.models.fields.related.OneToOneField')(related_name='project', unique=True, null=True, to=orm['main.Role'], blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('main', ['Project'])

        # Adding M2M table for field users on 'Project'
        db.create_table('main_project_users', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['main.project'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('main_project_users', ['project_id', 'user_id'])

        # Adding M2M table for field error_types on 'Project'
        db.create_table('main_project_error_types', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm['main.project'], null=False)),
            ('errortype', models.ForeignKey(orm['main.errortype'], null=False))
        ))
        db.create_unique('main_project_error_types', ['project_id', 'errortype_id'])

        # Deleting model 'Questionnaire'
        db.delete_table('main_questionnaire')

        # Removing M2M table for field users on 'Questionnaire'
        db.delete_table('main_questionnaire_users')

        # Removing M2M table for field error_types on 'Questionnaire'
        db.delete_table('main_questionnaire_error_types')

        # Deleting model 'ConfirmationQuestion'
        db.delete_table('main_confirmationquestion')

        # Adding field 'UIDStatus.project'
        db.add_column('main_uidstatus', 'project', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['main.Project']), keep_default=False)

        # Deleting field 'UIDStatus.questionnaire'
        db.delete_column('main_uidstatus', 'questionnaire_id')


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
        'main.confirmationquestion': {
            'Meta': {'object_name': 'ConfirmationQuestion'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subquestions'", 'null': 'True', 'to': "orm['main.ConfirmationQuestion']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
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
        'main.questionnaire': {
            'Meta': {'object_name': 'Questionnaire'},
            'error_types': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['main.ErrorType']", 'null': 'True', 'blank': 'True'}),
            'hierarchy': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'questionnaire'", 'unique': 'True', 'null': 'True', 'to': "orm['main.Role']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'main.role': {
            'Meta': {'object_name': 'Role'},
            'head': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'subordinate'", 'null': 'True', 'to': "orm['main.Role']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
            'completer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Role']", 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'errors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['main.ErrorType']", 'null': 'True', 'through': "orm['main.UIDError']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questionnaire': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['main.Questionnaire']"}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'uidstatuses'", 'null': 'True', 'to': "orm['main.Role']"}),
            'uid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        }
    }

    complete_apps = ['main']
