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

* ``form_kwargs``: Additional kwargs to be used in the creation of the form. Use with :class:`envelope.forms.BaseContactForm` form arguments for dynamic customization of the form.

To customize the email message sent to you, create a template called
``envelope/email_body.txt``. You can use any of the :class:`envelope.forms.ContactForm` field names as template variables.


.. _`FormView`: https://docs.djangoproject.com/en/dev/ref/class-based-views/#django.views.generic.edit.FormView

