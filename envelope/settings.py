# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Defaults and overrides for envelope-related settings.
"""

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


DEFAULT_CONTACT_CHOICES = (
    ('', _("Choose")),
    (10, _("A general question regarding the website")),
    (None, _("Other")),
)

FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

CONTACT_CHOICES = getattr(settings, 'ENVELOPE_CONTACT_CHOICES',
                          DEFAULT_CONTACT_CHOICES)

EMAIL_RECIPIENTS = getattr(settings, 'ENVELOPE_EMAIL_RECIPIENTS',
                           [settings.DEFAULT_FROM_EMAIL])

SUBJECT_INTRO = getattr(settings, 'ENVELOPE_SUBJECT_INTRO',
                        _("Message from contact form: "))

BASE_TEMPLATE = getattr(settings, 'ENVELOPE_BASE_TEMPLATE', 'base.html')

SUCCESS_URL = getattr(settings, 'ENVELOPE_SUCCESS_URL', 'envelope-contact-thanks')
FORM_CLASS = getattr(settings, 'ENVELOPE_FORM_CLASS', 'envelope.forms.ContactForm')
