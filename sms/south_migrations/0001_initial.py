# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
from django.conf import settings
import uuidfield.fields
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('base_url', models.URLField()),
                ('settings', jsonfield.fields.JSONField(help_text='A JSON Dictionary of key-value pairs that will be used for every message. Authorisation credentials should go in here, for example.', null=True, blank=True)),
                ('recipient_keyword', models.CharField(help_text='The keyword that is used in the request to identify the recipient number.', max_length=128)),
                ('content_keyword', models.CharField(max_length=128)),
                ('uuid_keyword', models.CharField(max_length=128, null=True, blank=True)),
                ('charge_keyword', models.CharField(max_length=128, null=True, blank=True)),
                ('status_mapping', jsonfield.fields.JSONField(null=True, blank=True)),
                ('status_msg_id', models.CharField(max_length=128, null=True, blank=True)),
                ('status_status', models.CharField(max_length=128, null=True, blank=True)),
                ('status_error_code', models.CharField(max_length=128, null=True, blank=True)),
                ('status_date', models.CharField(max_length=128, null=True, blank=True)),
                ('status_date_format', models.CharField(max_length=128, null=True, blank=True)),
                ('reply_content', models.CharField(max_length=128, null=True, blank=True)),
                ('reply_sender', models.CharField(max_length=128, null=True, blank=True)),
                ('reply_date', models.CharField(max_length=128, null=True, blank=True)),
                ('reply_date_format', models.CharField(default=b'%Y-%m-%d %H:%M:%S', max_length=128, null=True, blank=True)),
                ('success_format', models.CharField(help_text='A regular expression that parses the response', max_length=256, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(help_text='The body of the message.')),
                ('recipient_number', models.CharField(help_text='The international number of the recipient, without the leading +', max_length=32)),
                ('sender_number', models.CharField(help_text='The international number of the sender, without the leading +', max_length=32, null=True, blank=True)),
                ('send_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('delivery_date', models.DateTimeField(null=True, editable=False, blank=True)),
                ('uuid', uuidfield.fields.UUIDField(help_text='Used for associating replies.', unique=True, max_length=32, editable=False, blank=True)),
                ('status', models.CharField(default=b'Unsent', max_length=16, choices=[(b'Unsent', b'Unsent'), (b'Sent', b'Sent'), (b'Delivered', b'Delivered'), (b'Failed', b'Failed'), (b'No_Route', b'No_Route'), (b'Unauthorized', b'Unauthorized')])),
                ('status_message', models.CharField(max_length=128, null=True, blank=True)),
                ('billed', models.BooleanField(default=False)),
                ('object_id', models.PositiveIntegerField()),
                ('gateway_message_id', models.CharField(max_length=128, null=True, editable=False, blank=True)),
                ('reply_callback', picklefield.fields.PickledObjectField(null=True, editable=False, blank=True)),
                ('gateway_charge', models.DecimalField(null=True, max_digits=10, decimal_places=5, blank=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('gateway', models.ForeignKey(blank=True, to='sms.Gateway', null=True)),
                ('sender', models.ForeignKey(related_name=b'sent_sms_messages', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('send_date',),
                'permissions': (('view_message', 'Can view message'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text='Enter Provider Name', unique=True, max_length=255, verbose_name=b'Name')),
                ('description', models.TextField(help_text='Short description about Provider', verbose_name=b'Description')),
                ('metric', models.IntegerField(default=10, help_text='Enter metric in digit', verbose_name=b'Metric')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name=b'Date')),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Provider',
                'verbose_name_plural': 'Providers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('date', models.DateTimeField()),
                ('message', models.ForeignKey(related_name=b'replies', to='sms.Message')),
            ],
            options={
                'verbose_name_plural': 'replies',
            },
            bases=(models.Model,),
        ),
    ]
