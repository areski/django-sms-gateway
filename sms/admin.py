from django.contrib import admin
from sms.models import Gateway, Message, Reply

class GatewayAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

class ReplyAdmin(admin.ModelAdmin):
    pass
    
admin.site.register(Gateway, GatewayAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Reply, ReplyAdmin)
