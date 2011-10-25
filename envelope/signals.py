# -*- coding: utf-8 -*-

u"""
Signals sent by the application.
"""

from django.dispatch import Signal

before_send = Signal(providing_args=["request", "form"])
