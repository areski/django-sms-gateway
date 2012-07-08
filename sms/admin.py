from django.contrib import admin
from django.conf.urls.defaults import *
from django.utils.translation import ugettext as _
from sms.models import Gateway, Message, Reply, Provider


class GatewayAdmin(admin.ModelAdmin):
    search_fields = ('name', 'settings')
    list_display = ('name', 'base_url', 'settings', 'recipient_keyword',
                    'content_keyword', 'success_format',)

    def get_urls(self):
        urls = super(GatewayAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', self.admin_site.admin_view(self.changelist_view)),
            (r'^add/$', self.admin_site.admin_view(self.add_view)),
            (r'^/(.+)/$', self.admin_site.admin_view(self.change_view)),
        )
        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        """
        SMS Gateway Listing
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Select SMS Gateway to Change'),
        }
        return super(GatewayAdmin, self)\
               .changelist_view(request, extra_context=ctx)

    def add_view(self, request, extra_context=None):
        """
        Add SMS Gateway
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Add SMS Gateway'),
        }
        return super(GatewayAdmin, self).add_view(request, extra_context=ctx)

    def change_view(self, request, object_id, extra_context=None):
        """
        Edit Gateway
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Change SMS Gateway'),
        }
        return super(GatewayAdmin, self)\
               .change_view(request, object_id, extra_context=ctx)


class MessageAdmin(admin.ModelAdmin):
    search_fields = ('recipient_number', 'sender_number')
    list_display = ('id', 'recipient_number', 'sender', 'sender_number',
                    'send_date', 'delivery_date', 'uuid', 'status',
                    'status_message', 'billed', 'gateway')
    list_filter = ['send_date', 'status', 'sender', 'delivery_date',
                   'billed', 'gateway']

    def get_urls(self):
        urls = super(MessageAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', self.admin_site.admin_view(self.changelist_view)),
            (r'^add/$', self.admin_site.admin_view(self.add_view)),
            (r'^/(.+)/$', self.admin_site.admin_view(self.change_view)),
        )
        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        """
        Message Listing
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Select Message to Change'),
        }
        return super(MessageAdmin, self)\
               .changelist_view(request, extra_context=ctx)

    def add_view(self, request, extra_context=None):
        """
        Add Message
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Add Message'),
        }
        return super(MessageAdmin, self)\
               .add_view(request, extra_context=ctx)

    def change_view(self, request, object_id, extra_context=None):
        """
        Edit Message
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Change Message'),
        }
        return super(MessageAdmin, self)\
               .change_view(request, object_id, extra_context=ctx)


class ReplyAdmin(admin.ModelAdmin):
    list_display = ('content', 'message', 'date',)
    list_filter = ['date']

    def get_urls(self):
        urls = super(ReplyAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', self.admin_site.admin_view(self.changelist_view)),
            (r'^add/$', self.admin_site.admin_view(self.add_view)),
            (r'^/(.+)/$', self.admin_site.admin_view(self.change_view)),
        )
        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        """
        Reply Listing
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Select Reply to Change'),
        }
        return super(ReplyAdmin, self)\
               .changelist_view(request, extra_context=ctx)

    def add_view(self, request, extra_context=None):
        """
        Add Reply
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Add Reply'),
        }
        return super(ReplyAdmin, self)\
               .add_view(request, extra_context=ctx)

    def change_view(self, request, object_id, extra_context=None):
        """
        Edit Reply
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Change Reply'),
        }
        return super(ReplyAdmin, self)\
               .change_view(request, object_id, extra_context=ctx)


class ProviderAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Provider Detail'), {
            #'classes':('collapse', ),
            'fields': ('name', 'description', 'gateway', 'metric'),
        }),
    )
    list_display = ('id', 'name', 'gateway', 'metric', 'updated_date')
    list_display_links = ('name', )
    list_filter = ['gateway', 'metric']
    ordering = ('id', )

    def get_urls(self):
        urls = super(ProviderAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^$', self.admin_site.admin_view(self.changelist_view)),
            (r'^add/$', self.admin_site.admin_view(self.add_view)),
            (r'^/(.+)/$', self.admin_site.admin_view(self.change_view)),
        )
        return my_urls + urls

    def changelist_view(self, request, extra_context=None):
        """
        SMS Provider Listing
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Select SMS Provider to Change'),
        }
        return super(ProviderAdmin, self)\
               .changelist_view(request, extra_context=ctx)

    def add_view(self, request, extra_context=None):
        """
        Add SMS Provider
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Add SMS Provider'),
        }
        return super(ProviderAdmin, self)\
               .add_view(request, extra_context=ctx)

    def change_view(self, request, object_id, extra_context=None):
        """
        Edit Provider
        """
        ctx = {
            'app_label': _('SMS'),
            'title': _('Change SMS Provider'),
        }
        return super(ProviderAdmin, self)\
               .change_view(request, object_id, extra_context=ctx)


admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Reply, ReplyAdmin)
admin.site.register(Provider, ProviderAdmin)
