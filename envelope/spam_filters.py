# -*- coding: utf-8 -*-

u"""
Spam filters - functions that reject the message if it is considered spam.
"""

from honeypot.decorators import verify_honeypot_value


def check_honeypot(request, form):
    u"""
    ``verify_honeypot_value`` returns ``None`` when everything is OK.
    """
    return verify_honeypot_value(request, '') is None

