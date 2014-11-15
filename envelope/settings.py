# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Defaults and overrides for envelope-related settings.
"""

from django.conf import settings
from django.utils.translation import ugettext_lazy as _


FROM_EMAIL = settings.DEFAULT_FROM_EMAIL

EMAIL_RECIPIENTS = getattr(settings, 'ENVELOPE_EMAIL_RECIPIENTS',
                           [settings.DEFAULT_FROM_EMAIL])

SUBJECT_INTRO = getattr(settings, 'ENVELOPE_SUBJECT_INTRO',
                        _("Message from contact form: "))

USE_HTML_EMAIL = getattr(settings, 'ENVELOPE_USE_HTML_EMAIL', True)
