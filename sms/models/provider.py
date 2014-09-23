from django.db import models
from django.utils.translation import ugettext_lazy as _
from datetime import *


class Provider(models.Model):
    """
    Provider defines group or entity delivering SMS message
    Each provider will be associated to a Gateway which will link to the API of
    the Service Provider.
    """
    name = models.CharField(unique=True, max_length=255, verbose_name='Name',
                            help_text=_("Enter Provider Name"))
    description = models.TextField(verbose_name='Description',
                               help_text=_("Short description about Provider"))
    metric = models.IntegerField(default=10, verbose_name='Metric',
                                 help_text=_("Enter metric in digit"))
    # gateway = models.ForeignKey('sms.Gateway', null=True, blank=True,
    #                             help_text=_("Select Gateway"))
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        app_label = 'sms'
        verbose_name = _("Provider")
        verbose_name_plural = _("Providers")

    def __unicode__(self):
            return "%s" % self.name
