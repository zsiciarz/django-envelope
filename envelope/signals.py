# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Signals sent by the application.

``before_send``
---------------

    Sent after the form is submitted and valid, but before sending the message.

    Arguments:

    ``sender``
        View class.

    ``request``
        The current request object.

    ``form``
        The form object (already valid, so ``cleaned_data`` is available).

``after_send``
--------------

    This is sent after sending the message.

    Arguments:

    ``sender``
        Form class.

    ``message``
        An instance of :class:`EmailMessage <django.core.mail.EmailMessage>` that was used to send the message.

    ``form``
        The form object.
"""

from django.dispatch import Signal

before_send = Signal(providing_args=["request", "form"])
after_send = Signal(providing_args=["message", "form"])
