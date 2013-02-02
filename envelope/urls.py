# -*- coding: utf-8 -*-
try:
    # Django 1.5 and below.
    from django.conf.urls.defaults import patterns, url
except ImportError:
    # Django 1.6+
    from django.conf.urls import patterns, url

from envelope.views import ContactView


urlpatterns = patterns('',
    url(r'^$', ContactView.as_view(), name='envelope-contact'),
)

