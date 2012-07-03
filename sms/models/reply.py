from django.db import models

class Reply(models.Model):
    """
    A reply to a Message.
    """
    
    content = models.TextField()
    message = models.ForeignKey('sms.Message', related_name='replies')
    date = models.DateTimeField()
    
    class Meta:
        app_label = 'sms'
        verbose_name_plural = u'replies'
    
    