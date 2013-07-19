# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Signals sent by the application.
"""

from django.dispatch import Signal

before_send = Signal(providing_args=["request", "form"])
after_send = Signal(providing_args=["message", "form"])
