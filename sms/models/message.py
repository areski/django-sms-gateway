from django.db import models
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext as _
from django.conf import settings

import uuidfield.fields
import picklefield
if 'timezones' in settings.INSTALLED_APPS:
    from timezones.utils import adjust_datetime_to_timezone
else:
    def adjust_datetime_to_timezone(a,b,c):
        return a

from gateway import Gateway

class MessageManager(models.Manager):
    def get_matching_message(self, datadict):
        for gateway in Gateway.objects.all():
            try:
                return Message.objects.get(
                    gateway_message_id=datadict.get(gateway.status_msg_id),
                    gateway=gateway,
                )
            except Message.DoesNotExist:
                pass
    
    def get_original_for_reply(self, datadict):
        for gateway in Gateway.objects.all():
            try:
                return Message.objects.get(
                    uuid=datadict.get(gateway.uuid_keyword),
                    gateway=gateway
                )
            except Message.DoesNotExist:
                pass
        # This may have been a message sent from another phone, but
        # there may be a reply-code that was added in.
        return self.custom_reply_matcher(datadict)
    
    def custom_reply_matcher(self, datadict):
        # Designed to be overridden.
        return None
    
    def get_last_rate_for(self, recipient_number):
        m = Message.objects.filter(recipient_number=recipient_number).exclude(
            gateway_charge=None).order_by('-send_date')[0]
        return m.gateway_charge/m.length

MESSAGE_STATUSES = (
    ('Unsent', 'Unsent'),
    ('Sent', 'Sent'),
    ('Delivered', 'Delivered'),
    ('Failed', 'Failed'),
)
class Message(models.Model):
    """
    A Message.
    
    We have a uuid, which is our reference. We also have a gateway_message_id,
    which is their reference.  This is required by some systems so we can 
    pass in a unique value that will allow us to match up replies to original
    messages.
    """
    
    content = models.TextField(help_text=_(u'The body of the message.'))
    recipient_number = models.CharField(max_length=32, 
        help_text=_(u'The international number of the recipient, without the leading +'))
    
    sender = models.ForeignKey('auth.User', related_name='sent_sms_messages')
    send_date = models.DateTimeField(null=True, blank=True, editable=False)
    delivery_date = models.DateTimeField(null=True, blank=True, editable=False)
    uuid = uuidfield.fields.UUIDField(auto=True, help_text=_(u'Used for associating replies.'))
    
    status = models.CharField(max_length=16, choices=MESSAGE_STATUSES,
        default="Unsent",
    )
    status_message = models.CharField(max_length=128, null=True, blank=True)
    billed = models.BooleanField(default=False)
    
    content_type = models.ForeignKey('contenttypes.ContentType')
    object_id = models.PositiveIntegerField()
    billee = generic.GenericForeignKey()
    
    gateway = models.ForeignKey('sms.Gateway', 
        null=True, blank=True, editable=False)
    gateway_message_id = models.CharField(max_length=128, 
        blank=True, null=True, editable=False)
    
    reply_callback = picklefield.PickledObjectField(null=True, blank=True)
    
    gateway_charge = models.DecimalField(max_digits=10, decimal_places=5,
        null=True, blank=True)
    
    objects = MessageManager()
    
    class Meta:
        app_label = 'sms'
        permissions = (
            ('view_message', 'Can view message'),
        )
        ordering = ('send_date',)
    
    def send(self, gateway):
        gateway.send(self)
    
    @property
    def length(self):
        """Unicode messages are limited to 70 chars/message segment."""
        # try:
        #     return len(str(self.content)) / 160 + 1
        # except UnicodeEncodeError:
        #     return len(self.content) / 70 + 1
        return len(self.content) / 160 + 1
    
    @property
    def local_send_time(self):
        if self.billee.timezone:
            return adjust_datetime_to_timezone(
                self.send_date, 
                settings.TIME_ZONE, 
                self.billee.timezone
            )
        return self.send_date
            
    def __unicode__(self):
        return "[%s] Sent to %s by %s at %s [%i]" % (
            self.status,
            self.recipient_number,
            self.sender,
            self.send_date,
            self.length
        )