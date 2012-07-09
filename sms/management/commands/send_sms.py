from django.core.management.base import BaseCommand
from optparse import make_option
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from sms.models import Gateway, Message


class Command(BaseCommand):
    args = ' gatewayid, message, recipient '
    help = "Send SMS\n" \
           "---------------------------------\n" \
           "python manage.py send_sms --gatewayid=1 --message=Hello+World " \
           "--recipient=+34650234032"

    option_list = BaseCommand.option_list + (
        make_option('--gatewayid',
                    default=None,
                    dest='gatewayid',
                    help=help),
        make_option('--message',
                    default=None,
                    dest='message',
                    help=help),
        make_option('--recipient',
                    default=None,
                    dest='recipient',
                    help=help),
        )

    def handle(self, *args, **options):
        """
        Handle SMS Sending
        """
        arg_gatewayid = 1  # default
        if options.get('gatewayid'):
            try:
                arg_gatewayid = int(options.get('gatewayid'))
            except ValueError:
                arg_gatewayid = 1

        arg_message = 'Hello World'  # default
        if options.get('message'):
            arg_message = options.get('message')

        arg_recipient = False  # default
        if options.get('recipient'):
            try:
                arg_recipient = options.get('recipient')
                arg_recipient = int(arg_recipient)
            except ValueError:
                arg_recipient = 0

        print "Preparing to send SMS (%d, %s, %s)" % (
                        arg_gatewayid,
                        arg_message,
                        arg_recipient)

        #Retrieve ContentType
        content_type = ContentType.objects\
                .get(app_label=str('sms'), model=str('message'))
        object_id = 1

        #Get Gateway
        gateway = Gateway.objects.get(pk=arg_gatewayid)

        #Get First User
        admin_user = User.objects.get(pk=1)

        #Create Message
        new_msg = Message.objects.create(
                    content=arg_message,
                    recipient_number=arg_recipient,
                    sender=admin_user,
                    content_type=content_type,
                    object_id=object_id,
                    gateway=gateway)
        print new_msg

        #Send Message
        gateway._send(new_msg)
