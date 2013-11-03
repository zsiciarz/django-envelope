=========
Reference
=========

Views
=====

.. automodule:: envelope.views
   :members:

Forms
=====

.. automodule:: envelope.forms
   :members:

Template tags
=============

Add ``{% load envelope_tags %}`` to your template before using any of these.

.. automodule:: envelope.templatetags.envelope_tags
   :members:

Spam filters
============

.. automodule:: envelope.spam_filters
   :members:

Signals
=======

``before_send``

    Sent after the form is submitted and valid, but before sending the message.

    Arguments:

    ``sender``
        View class.

    ``request``
        The current request object.

    ``form``
        The form object (already valid, so ``cleaned_data`` is available).

``after_send``

    This signal is sent after sending the message.

    Arguments:

    ``sender``
        Form class.

    ``message``
        An instance of :class:`EmailMessage <django.core.mail.EmailMessage>` that was used to send the message.

    ``form``
        The form object.
