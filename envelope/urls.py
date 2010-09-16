# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

urlpatterns = patterns('envelope.views',
    url(r'^$',         'contact',    name='envelope-contact'),
)
