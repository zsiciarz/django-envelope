=============
Customization
=============

Most of the time, including ``envelope.urls`` is just fine. But if you want more
control over the contact form, you need to hook the view into your URLconf
yourself. Just import :class:`envelope.views.ContactView`, and call the
``as_view`` classmethod when defining URL patterns.

Example::

    # urls.py
    from django.conf.urls import patterns, url
    from envelope.views import ContactView

    urlpatterns = patterns('',
        url(r'^contact/', ContactView.as_view()),
    )

.. _subclassing-contact-view:

If you want some more fine-grained control over the contact form, you can
customize the view class. You can inherit from :class:`envelope.views.ContactView`
and set class attributes in your derived view class, or simply pass
the values for these attributes when calling ``as_view`` in your URLconf.

Example (using a subclass)::

    # some_app/views.py
    from envelope.views import ContactView

    class MyContactView(ContactView):
        template_name = "my_contact.html"
        success_url = "/thank/you/kind/sir/"

    # urls.py
    from django.conf.urls import patterns, url
    from some_app.views import MyContactView

    urlpatterns = patterns('',
        url(r'^contact/', MyContactView.as_view()),
    )

Example (setting attributes in place)::

    # urls.py
    from django.conf.urls import patterns, url
    from envelope.views import ContactView

    urlpatterns = patterns('',
        url(r'^contact/', ContactView.as_view(
            template_name="my_contact.html",
            success_url="/thank/you/kind/sir/"
        )),
    )

The following options (as well as those already in Django's `FormView`_) are recognized by the view:

* ``form_class``: Which form class to use for contact message handling.
  The default (:class:`envelope.forms.ContactForm`) is often enough, but you can subclass it
  if you want, or even replace with a totally custom class. The only requirement is
  that your custom class has a ``save()`` method which should send the message
  somewhere. Stick to the default, or its subclasses.

* ``template_name``: Full name of the template which will display the form. By
  default it is ``envelope/contact.html``.

* ``success_url``: View name or a hardcoded URL of the page with some kind of a
  "thank you for your feedback", displayed after the form is successfully
  submitted. If left unset, the view redirects to itself.

* ``form_kwargs``: Additional kwargs to be used in the creation of the form. Use with :class:`envelope.forms.ContactForm` form arguments for dynamic customization of the form.

You can also subclass :class:`envelope.forms.ContactForm` to further customize
your form processing. Either set the following options as keyword arguments to
``__init__``, or override class attributes.

* ``subject_intro``: Prefix used to create the subject line. Default is ``settings.ENVELOPE_SUBJECT_INTRO``.

* ``from_email``: Used in the email from. Defaults to ``settings.DEFAULT_FROM_EMAIL``.

* ``email_recipients``: List of email addresses to send the email to. Defaults to ``settings.ENVELOPE_EMAIL_RECIPIENTS``.

* ``template_name``: Template used to render the plaintext email message. Defaults to ``envelope/email_body.txt``. You can use any of the form field names as template variables.

* ``html_template_name``: Template used to render the HTML email message. Defaults to ``envelope/email_body.html``.

Example of a custom form::

    # forms.py
    from envelope.forms import ContactForm

    class MyContactForm(ContactForm):
        subject_intro = "URGENT: "
        template_name = "plaintext_email.txt"
        html_template_name = "contact_email.html"

    # urls.py
    from django.conf.urls import patterns, url
    from envelope.views import ContactView
    from forms import MyContactForm

    urlpatterns = patterns('',
        url(r'^contact/', ContactView.as_view(form_class=MyContactForm)),
    )


.. _`FormView`: https://docs.djangoproject.com/en/dev/ref/class-based-views/#django.views.generic.edit.FormView

