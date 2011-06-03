=============
Customization
=============

TODO: Write docs about class-based approach.

.. note::
    The function-based view :func:`envelope.views.contact` is **deprecated**
    since django-envelope 0.3.0. New projects should use
    :class:`envelope.views.ContactView` instead.

If you want some more fine-grained control over the contact form, you can
supply additional optional arguments to the view function. Instead of including
the application's URLconf, hook the :func:`envelope.views.contact` view into your
``urls.py``. The following optional arguments are recognized by the view function:

* ``form_class``: Which form class to use for contact message handling.
  The default (:class:`envelope.forms.ContactForm`) is often enough, but you can subclass it
  if you want, or even replace with a totally custom class. The only requirement is
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
``envelope/email_body.txt``. You can use any of the :class:`envelope.forms.ContactForm` field names as template variables. 

