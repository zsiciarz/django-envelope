# -*- coding: utf-8 -*-

u"""
Functions that reject the message if it is considered spam.
"""

from honeypot.decorators import verify_honeypot_value


def check_honeypot(request, form):
    u"""
    Make sure that the hidden form field is empty, using django-honeypot.
    """
    return verify_honeypot_value(request, '') is None
