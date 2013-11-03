# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Functions that reject the message if it is considered spam.
"""


def check_honeypot(request, form):
    """
    Make sure that the hidden form field is empty, using django-honeypot.
    """
    try:
        from honeypot.decorators import verify_honeypot_value
        return verify_honeypot_value(request, '') is None
    except ImportError:  # pragma: no cover
        return True
