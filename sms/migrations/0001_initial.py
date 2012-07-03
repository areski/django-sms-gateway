# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Gateway'
        db.create_table('sms_gateway', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('base_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('settings', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('recipient_keyword', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content_keyword', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('uuid_keyword', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('status_mapping', self.gf('jsonfield.fields.JSONField')(null=True, blank=True)),
            ('status_msg_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('status_status', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('status_error_code', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('status_date', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('status_date_format', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('reply_content', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('reply_sender', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('reply_date', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('reply_date_format', self.gf('django.db.models.fields.CharField')(default='%Y-%m-%d %H:%M:%S', max_length=128, null=True, blank=True)),
            ('success_format', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('sms', ['Gateway'])

        # Adding model 'Message'
        db.create_table('sms_message', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('recipient_number', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(related_name='sent_sms_messages', to=orm['auth.User'])),
            ('send_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('delivery_date', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('uuid', self.gf('uuidfield.fields.UUIDField')(max_length=32, auto=True, null=True, blank=True)),
            ('status', self.gf('django.db.models.fields.CharField')(default='Unsent', max_length=16)),
            ('status_message', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('billed', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('gateway', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sms.Gateway'], null=True, blank=True)),
            ('gateway_message_id', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('reply_callback', self.gf('picklefield.fields.PickledObjectField')(null=True, blank=True)),
        ))
        db.send_create_signal('sms', ['Message'])

        # Adding model 'Reply'
        db.create_table('sms_reply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replies', to=orm['sms.Message'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('sms', ['Reply'])


    def backwards(self, orm):
        
        # Deleting model 'Gateway'
        db.delete_table('sms_gateway')

        # Deleting model 'Message'
        db.delete_table('sms_message')

        # Deleting model 'Reply'
        db.delete_table('sms_reply')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sms.gateway': {
            'Meta': {'object_name': 'Gateway'},
            'base_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'content_keyword': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'recipient_keyword': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'reply_content': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'reply_date': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'reply_date_format': ('django.db.models.fields.CharField', [], {'default': "'%Y-%m-%d %H:%M:%S'", 'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'reply_sender': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'settings': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'status_date': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status_date_format': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status_error_code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status_mapping': ('jsonfield.fields.JSONField', [], {'null': 'True', 'blank': 'True'}),
            'status_msg_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status_status': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'success_format': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'uuid_keyword': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'})
        },
        'sms.message': {
            'Meta': {'object_name': 'Message'},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'delivery_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'gateway': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sms.Gateway']", 'null': 'True', 'blank': 'True'}),
            'gateway_message_id': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'recipient_number': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'reply_callback': ('picklefield.fields.PickledObjectField', [], {'null': 'True', 'blank': 'True'}),
            'send_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sent_sms_messages'", 'to': "orm['auth.User']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Unsent'", 'max_length': '16'}),
            'status_message': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'uuid': ('uuidfield.fields.UUIDField', [], {'max_length': '32', 'auto': 'True', 'null': 'True', 'blank': 'True'})
        },
        'sms.reply': {
            'Meta': {'object_name': 'Reply'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replies'", 'to': "orm['sms.Message']"})
        }
    }

    complete_apps = ['sms']
