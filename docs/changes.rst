=========
Changelog
=========

1.4.0
-----

 - fixed french translation
 - Python 3.7, 3.8 and Django 2.2, 3.0 compatibility

1.3.0
-----

 - added Greek translation, thanks raratiru!
 - Python 3.6 and Django 1.11 compatibility

1.2.0
-----

 - added Latvian and Russian translations, thanks wildd!
 - added Spanish translations, thanks javipalanca!

1.1.0
-----

 - added Brazilian Portuguese translation, thanks aleprovencio!
 - Python 3.5 and Django 1.9 compatibility


1.0.0
-----

Improvements and fixes:
 - HTML email support
 - subject field is optional by default
 - support for `custom User model`_
 - docs: added :doc:`cookbook`

Backwards incompatible changes:
 - removed category field from :class:`~envelope.forms.ContactForm`
 - ``BaseContactForm`` no longer exists; to customize form processing, subclass
   :class:`~envelope.forms.ContactForm` directly
 - :class:`~envelope.views.ContactView` does not create any flash messages;
   use `FormMessagesMixin`_ from  `django-braces`_ (see the :doc:`cookbook`
   for an example)
 - dropped Django 1.4 compatibility
 - dropped Python 2.6 compatibility; use 2.7 or 3.3+
 - message rejection reason from signal handlers isn't sent to the user in
   HTTP 400 response's body
 - the default ``envelope/contact.html`` template is removed; one must create
   the template explicitly

.. _`custom User model`: https://docs.djangoproject.com/en/dev/topics/auth/customizing/#substituting-a-custom-user-model
.. _`FormMessagesMixin`: http://django-braces.readthedocs.org/en/latest/form.html#formmessagesmixin
.. _`django-braces`: https://github.com/brack3t/django-braces

0.7.0
-----
 - added :func:`{% render_contact_form %} <envelope.templatetags.envelope_tags.render_contact_form>`
   template tag
 - Django 1.6 compatibility
 - settled on 3.3 as the minimum supported Python 3 version
 - moved to Travis CI as the continuous integration solution

0.6.1
-----
 - fixed ``NameError`` in example project

0.6.0
-----
 - Python 3 compatibility!

0.5.1
-----
 - fixed template loading in tests

0.5.0
-----
 - contact form class is more customizable
 - the ``Reply-To`` header in the message is set to whatever the submitted
   email was
 - added ``after_send`` signal
 - `django-honeypot`_ is now just an optional dependency
 - ``example_project`` is no longer incorrectly distributed with the application

.. _`django-honeypot`: https://github.com/sunlightlabs/django-honeypot

0.4.1
-----
 - security bugfix regarding initial form values

0.4.0
-----
 - removed the function-based view
 - removed ``ContactForm.send()`` method
 - application signals (``before_send``)
 - updated documentation
 - reworked settings
 - Continous Integration server, thanks to ShiningPanda

0.3.2
-----
 - omit the brackets if the user doesn't have a full name
 - honeypot is mentioned in the usage docs

0.3.1
-----
 - configurable recipients
 - better logging hierarchy
 - the code is more PEP-8 compliant

0.3.0
-----
 - introduced a class-based :class:`envelope.views.ContactView` (requires
   Django >= 1.3)
 - deprecated the function-based view ``envelope.views.contact``
 - improved test coverage
 - more and better documentation (also hosted on Read The Docs)

0.2.1
-----
 - French translation added

0.2.0
-----
 - deprecated the ``ContactForm.send()`` method, use
   :meth:`envelope.forms.ContactForm.save`  instead for more consistency
   with Django coding style
 - localization support

0.1.4
-----
 - added a more descriptive README file

0.1.3
-----
 - added the ``redirect_to`` optional argument to view function

0.1.2
-----
 - added the ``extra_context`` argument to view function

0.1.1
-----
 - improved setup script, added dependencies

0.1.0
-----
 - initial version
