===============
django-envelope
===============

``django-envelope`` is a simple contact form app for Django web framework.

The application provides a simple contact form and a Django view to handle
form submission.

Installation
============

Make sure you have Django installed. Then install the package from PyPI::

    pip install django-envelope
    
or::

    easy_install django-envelope

This should download and install ``django-envelope``, along with it's 
dependencies (currently only ``django-honeypot``).

If you like living on the edge, grab the development version from Github_::

    git clone git://github.com/zsiciarz/django-envelope.git
    cd django-envelope
    python setup.py install
    
.. _Github: http://github.com/zsiciarz/django-envelope

Usage
=====

Add ``envelope`` to your ``INSTALLED_APPS`` in ``settings.py``. The application
does not define any models, so a ``manage.py syncdb`` is *not needed*. 

For a quick start, simply include the app's ``urls.py`` in your main URLconf, like
this::

    urlpatterns = patterns('',
        #...
        (r'^contact/',    include('envelope.urls')),
        #...
    )

That's basically it. Navigate to the given URL and see the contact form in
action. See below for more customization options.

Configuration
=============

These values defined in ``settings.py`` affect the application:

* ``DEFAULT_FROM_EMAIL``: This is both the sender **and** the recipient of
  the email sent with your contact form. Some web servers do not allow
  sending messages from an address that is different than the one used for
  SMTP authentication.

* ``ENVELOPE_CONTACT_CHOICES``: A tuple of pairs describing possible choices
  for message type. The default is defined as follows::
  
    DEFAULT_CONTACT_CHOICES = (
        ('',    u"Choose"),
        (10,    u"A general question regarding the website"),
        (None,   u"Other"),
    )
  
  The numeric values are pretty much arbitrary. Remember to leave an empty
  value for the choice when the field is initially unset ("Choose").

* ``ENVELOPE_SUBJECT_INTRO``: The prefix for subject line of the email message.
  This is different than ``EMAIL_SUBJECT_PREFIX`` which is global for the whole
  project. ``ENVELOPE_SUBJECT_INTRO`` goes after the global prefix and is
  followed by the actual subject entered in the form by website's user.
  
  Default value: *Message from contact form:*

Customization
=============

If you want some more fine-grained control over the contact form, you can
supply additional optional arguments to the view function. Instead of including
the application's URLconf, hook the ``envelope.views.contact`` view into your
``urls.py``. The following optional arguments are recognized by the view function:

* ``form_class``: Which form class to use for contact message handling.
  The default (``ContactForm``) is often enough, but you can subclass it if you
  want, or even replace with a totally custom class. The only requirement is
  that your custom class has a ``save()`` method which should send the message
  somewhere. Stick to the default, or its subclasses.

* ``template_name``: Full name of the template which will display the form. By
  default it is ``envelope/contact.html``.

* ``redirect_to``: View name or a hardcoded URL of the page with some kind of a
  "thank you for your feedback", displayed after the form is successfully 
  submitted. If left unset, the view redirects to itself.

* ``extra_context``: A dictionary of values to add to template context.

Example::

    from my_app.forms import MyContactForm
    
    contact_info = {
        'form_class':       MyContactForm,
        'template_name':    'my_contact.html',
        'redirect_to':      '/thanks/',
    }
    urlpatterns = patterns('',
        #...
        url(r'^contact/', 
            'envelope.views.contact',
            kwargs=contact_info,
            name='envelope-contact'
        ),
        #...
    )

To customize the email message sent to you, create a template called 
``envelope/email_body.txt``. You can use any of the ``ContactForm`` field names
as template variables. 


License
=======
django-envelope is free software, licensed under the MIT/X11 License. A copy of
the license is provided with the application in the LICENSE file.

Author
======

Zbigniew Siciarz (antyqjon atty gmail dotty com)
