=====
Usage
=====

Add ``envelope`` to your ``INSTALLED_APPS`` in ``settings.py``. The application
does not define any models, so a ``manage.py syncdb`` is *not needed*. If you
installed ``django-honeypot``, add also ``honeypot`` to ``INSTALLED_APPS``.

For a quick start, simply include the app's ``urls.py`` in your main URLconf, like
this::

    urlpatterns = patterns('',
        #...
        (r'^contact/',    include('envelope.urls')),
        #...
    )

The view that you just hooked into your URLconf will try to render a
``envelope/contact.html`` template. Create that file in some location
where Django would be able to find it (see the `Django template docs`_
for details).

.. note::
   .. versionchanged:: 1.0
      ``django-envelope`` used to ship with one such template by default.
      However, it made too opinionated assumptions about your templates and
      site layout. For that reason it was removed and you *must* now create
      the template explicitly.

This template file can (and possibly should) extend your base site template.
The view will pass to the context a ``form`` variable, which is an instance
of :class:`~envelope.forms.ContactForm`. You can write your own HTML code
for the form or use the provided ``{% render_contact_form %}`` template tag
for simplicity. For example (assuming ``base.html`` is your main template):

.. code-block:: html+django

    {% extends "base.html" %}
    {% load envelope_tags %}

    {% block content %}
        {% render_contact_form %}
    {% endblock %}

That's basically it. Navigate to the given URL and see the contact form in
action. See :doc:`customization` for more customization options.

.. _`Django template docs`: https://docs.djangoproject.com/en/dev/ref/templates/api/#loading-templates
