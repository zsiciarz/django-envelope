# -*- coding: utf-8 -*-

try:
    # Django 1.6+
    from django.conf.urls import patterns, url
except ImportError:  # pragma: no cover
    # Django 1.4 and 1.5
    from django.conf.urls.defaults import patterns, url

from envelope.views import ContactView, ThanksView


urlpatterns = patterns('',
    url(r'^$', ContactView.as_view(), name='envelope-contact'),
    url(r'^thanks/$', ThanksView.as_view(), name='envelope-contact-thanks'),
)
