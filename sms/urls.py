from django.conf.urls.defaults import patterns, url

import views

urlpatterns = patterns('',
    url('^status_postback/$', views.update_delivery_status, name='status_postback'),
    url('^reply_postback/$', views.handle_reply, name='reply_postback'),
)