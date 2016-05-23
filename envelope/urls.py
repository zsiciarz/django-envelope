# -*- coding: utf-8 -*-

from django.conf.urls import url

from envelope.views import ContactView


urlpatterns = [
    url(r'^$', ContactView.as_view(), name='envelope-contact'),
]
