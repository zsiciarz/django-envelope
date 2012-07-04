# -*- coding: utf-8 -*-

u"""
Functions that reject the message if it is considered spam.
"""


def check_honeypot(request, form):
    u"""
    Make sure that the hidden form field is empty, using django-honeypot.
    """
    try:
        from honeypot.decorators import verify_honeypot_value
        return verify_honeypot_value(request, '') is None
    except ImportError:
        return True
