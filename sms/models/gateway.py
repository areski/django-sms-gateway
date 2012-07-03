from django.db import models
import jsonfield
import urllib
import datetime
from django.utils.translation import ugettext as _
import logging
import re
import unicodedata

from django.conf import settings

class Gateway(models.Model):
    """
    A Gateway is a sending endpoint, and associated authentication info
    that can be used to send and receive messages.
    """
    
    name = models.CharField(max_length=128)
    base_url = models.URLField()
    settings = jsonfield.fields.JSONField(null=True, blank=True,
        help_text=_(u'A JSON Dictionary of key-value pairs that will be '
            'used for every message. Authorisation credentials should go '
            'in here, for example.'
        ))
    recipient_keyword = models.CharField(max_length=128,
        help_text=_(u'The keyword that is used in the request to identify the recipient number.')
    )
    content_keyword = models.CharField(max_length=128)
    uuid_keyword = models.CharField(max_length=128, null=True, blank=True)
    charge_keyword = models.CharField(max_length=128, null=True, blank=True)
    
    status_mapping = jsonfield.JSONField(null=True, blank=True)
    
    status_msg_id = models.CharField(max_length=128, null=True, blank=True)
    status_status = models.CharField(max_length=128, null=True, blank=True)
    status_error_code = models.CharField(max_length=128, null=True, blank=True)
    status_date = models.CharField(max_length=128, null=True, blank=True)
    status_date_format = models.CharField(max_length=128, null=True, blank=True)
    
    reply_content = models.CharField(max_length=128, null=True, blank=True)
    reply_sender = models.CharField(max_length=128, null=True, blank=True)
    reply_date = models.CharField(max_length=128, null=True, blank=True)
    reply_date_format = models.CharField(max_length=128, null=True, blank=True,
        default="%Y-%m-%d %H:%M:%S")
    
    success_format = models.CharField(max_length=256, null=True, blank=True,
        help_text=_(u'A regular expression that parses the response'))
    
#     check_number_url = models.CharField(max_length=256, null=True, blank=True,
#         help_text=_(u'The URL that can be used to check availability of sending to a number'))
#     check_number_field = models.CharField(max_length=65, null=True, blank=True,
#         help_text=_(u'The keyword that contains the number to check'))
#     check_number_response_format = models.CharField(max_length=256, null=True, blank=True,
#         help_text=_(u'A regular expression that parses the response. Keys: status, charge'))
#     check_number_status_mapping = jsonfield.JSONField(null=True, blank=True)
    
    class Meta:
        app_label = 'sms'
    
    def __unicode__(self):
        return self.name
    
    def send(self, message):
        """
        Use this gateway to send a message.
        
        If ``celery`` is installed, then we assume they have set up the
        ``celeryd`` server, and we queue for delivery. Otherwise, we will
        send in-process.
        
        .. note::
            It is strongly recommended to run this out of process, 
            especially if you are sending as part of an HttpRequest, as this
            could take ~5 seconds per message that is to be sent.
        """
        if 'celery' in settings.INSTALLED_APPS:
            import sms.tasks
            sms.tasks.SendMessage.delay(message.pk, self.pk)
        else:
            self._send(message)
        
    def _send(self, message):
        """
        Actually do the work of sending the message. This is in a seperate
        method so we can background it it possible.
        """
        assert message.status == "Unsent", "Re-sending SMS Messages not yet supported."
        # We need to store the gateway that was used, so we can match up
        # which gateway a reply has come through.
        message.gateway = self
        # Build up a URL-encoded request.
        raw_data = {}
        raw_data.update(**self.settings)
        if message.recipient_number:
            raw_data[self.recipient_keyword] = message.recipient_number
        else:
            raise ValueError("A recipient_number must be supplied")
        # We need to see if this message needs to be sent as unicode.
        # Could be smart and try to see if it is a short enough message.
        # Or look for a preference that says if this person may send unicode
        # messages?
        # try:
        #     str(message.content)
        # except UnicodeEncodeError:
        #     raw_data[self.content_keyword] = "".join(["%04x" % ord(x) for x in message.content])
        #     raw_data["unicode"] = 1
        # else:
        raw_data[self.content_keyword] = unicodedata.normalize('NFKD', unicode(message.content)).encode('ascii', 'ignore')
        if self.uuid_keyword:
            assert message.uuid, "Message must have a valid UUID. Has it been saved?"
            raw_data[self.uuid_keyword] = message.uuid
        data = urllib.urlencode(raw_data)
        logging.debug(data)
        logging.debug(self)
        # Now hit the server.
        res = urllib.urlopen(self.base_url, data)
        
        # Most servers will respond with something, which is only an
        # interim status, which we can get for now, and maybe update later.
        status_msg = res.read()
        logging.debug(status_msg)
        if status_msg.startswith('ERR') or status_msg.startswith('WARN'):
            message.status = "Failed"
            message.status_message = status_msg.split(': ')[1]
        else:
            message.status = "Sent"
            parsed_response = re.match(self.success_format, status_msg).groupdict()
            if 'gateway_message_id' in parsed_response and parsed_response['gateway_message_id']:
                message.gateway_message_id = parsed_response['gateway_message_id'].strip()
            if 'status_code' in parsed_response and parsed_response['status_code']:
                message.status = self.status_mapping.get(parsed_response['status_code'])
            if 'status_message' in parsed_response and parsed_response['status_message']:
                message.status_message = parsed_response['status_message']
            logging.debug("Gateway MSG ID %s [%i]" % (message.gateway_message_id, len(message.gateway_message_id)))
            message.send_date = datetime.datetime.now()
        
        message.save()
        
        return message
    
    def check_availability_to_send(self, number):
        if not self.check_number_url:
            return None
            
        raw_data = {}
        raw_data.update(**self.settings)
        raw_data[self.check_number_field] = number
        data = urllib.urlencode(raw_data)
        res = urllib.urlopen(self.check_number_url, data)
        res_data = res.read()
        
        if self.check_number_response_format:
            parsed_response = re.match(self.check_number_response_format, res_data).groupdict()
            status = self.check_number_status_mapping.get(parsed_response.get('status', None), None)
            charge = self.check_number_status_mapping.get(parsed_response.get('charge', None), None)
            
            