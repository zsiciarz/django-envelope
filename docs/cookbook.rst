========
Cookbook
========

Success and error messages
==========================

Starting from release 1.0, :class:`envelope.views.ContactView` does not set any
`messages`_ since these were customized by most users anyway. We encourage
you to use the excellent `django-braces`_ app which provides a
`FormMessagesMixin`_ designed specifically for this purpose.

.. _`messages`: https://docs.djangoproject.com/en/dev/ref/contrib/messages/
.. _`django-braces`: https://github.com/brack3t/django-braces
.. _`FormMessagesMixin`: http://django-braces.readthedocs.org/en/latest/form.html#formmessagesmixin

The following example shows how to add the mixin to ``ContactView``::

    from braces.views import FormMessagesMixin
    from envelope.views import ContactView

    from django.utils.translation import ugettext_lazy as _


    class MyContactView(FormMessagesMixin, ContactView):
        form_valid_message = _(u"Thank you for your message.")
        form_invalid_message = _(u"There was an error in the contact form.")

See the :ref:`customization section <subclassing-contact-view>` on how to plug
the subclassed view into your URLconf.

Check out `Django messages documentation`_ to make sure messages are enabled in your project.

.. _`Django messages documentation`: https://docs.djangoproject.com/en/dev/ref/contrib/messages/#enabling-messages

Bootstrap integration
=====================

Embedding the contact form
--------------------------

From our personal experience with `Bootstrap`_-powered websites, the easiest
way to embed the contact form is to use `django-crispy-forms`_. Install it
with::

    pip install django-crispy-forms

and add ``crispy_forms`` to ``INSTALLED_APPS``. From there it's as simple as
adding a ``crispy`` template tag to display the form. For example:

.. code-block:: html+django

    {% load envelope_tags crispy_forms_tags %}

    ...

    <form action="{% url 'envelope-contact' %}" method="post">
        {% csrf_token %}
        {% antispam_fields %}
        {% crispy form %}
    </form>

.. _`Bootstrap`: http://getbootstrap.com/
.. _`django-crispy-forms`: https://github.com/maraujop/django-crispy-forms

To add a submit button, create a custom form using ``django-crispy-forms`` helper::

    # forms.py
    from envelope.forms import ContactForm
    from crispy_forms.helper import FormHelper
    from crispy_forms.layout import Submit


    class MyContactForm(ContactForm):
        def __init__(self, *args, **kwargs):
            super(MyContactForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Submit('submit', 'Submit', css_class='btn-lg'))

And finally link this form to your view::

    # views.py
    from braces.views import FormMessagesMixin
    from envelope.views import ContactView

    from django.utils.translation import ugettext_lazy as _

    from .forms import MyContactForm


    class MyContactView(FormMessagesMixin, ContactView):
        form_invalid_message = _(u"There was an error in the contact form.")
        form_valid_message = _(u"Thank you for your message.")
        form_class = MyContactForm

or just use it in your urls.py if you directly reference :class:`~envelope.views.ContactView` ``as_view()`` method::

    # urls.py
    from django.conf.urls import patterns, url
    from envelope.views import ContactView

    from .forms import MyContactForm


    urlpatterns = patterns('',
        url(r'^contact/', ContactView.as_view(form_class=MyContactForm)),
    )

Displaying form messages nicely
-------------------------------

GETting the contact form page after POSTing it will give you access to either a success message (form_valid_message)
or an error message (form_invalid_message) thanks to django-braces' ``FormMessagesMixin``. These messages use
`Django messages tag level`_ so you can use the right Bootstrap class.

.. _`Django messages tag level`: https://docs.djangoproject.com/en/dev/ref/contrib/messages/#message-tags

We recommend you first override Django's default message tags as following::

    # settings.py
    MESSAGE_TAGS = {
        messages.DEBUG: 'debug',
        messages.INFO: 'info',
        messages.SUCCESS: 'success',
        messages.WARNING: 'warning',
        messages.ERROR: 'danger' # 'error' by default
    }

Then you can use `Django's tip`_ to display messages with Bootstrap CSS classes such as text-info or alert-warning:

.. _`Django's tip`: https://docs.djangoproject.com/en/dev/ref/contrib/messages/#displaying-messages

.. code-block:: html+django

    {% if messages %}
        <ul class="messages">
            {% for message in messages %}
                <li {% if message.tags %} class="text-{{ message.tags }}"{% endif %}>
                    {{ message }}
                </li>
            {% endfor %}
        </ul>
    {% endif %}

Categorized contact form
========================

Although the ``category`` field was removed from the default form class in
1.0, you can bring it back to your form using the following subclass::

    from envelope.forms import ContactForm

    from django import forms
    from django.utils.translation import ugettext_lazy as _


    class CategorizedContactForm(ContactForm):
        CATEGORY_CHOICES = (
            ('', _("Choose")),
            (10, _("A general question regarding the website")),
            # ... any other choices you can imagine
            (None, _("Other")),
        )
        category = forms.ChoiceField(label=_("Category"), choices=CATEGORY_CHOICES)

        def __init__(self, *args, **kwargs):
            """
            Category choice will be rendered above the subject field.
            """
            super(CategorizedContactForm, self).__init__(*args, **kwargs)
            self.fields.keyOrder = [
                'sender', 'email', 'category', 'subject', 'message',
            ]

        def get_context(self):
            """
            Adds full category description to template variables in order
            to display the category in email body.
            """
            context = super(CategorizedContactForm, self).get_context()
            context['category'] = self.get_category_display()
            return context

        def get_category_display(self):
            """
            Returns the displayed name of the selected category.
            """
            try:
                category = int(self.cleaned_data['category'])
            except (AttributeError, ValueError, KeyError):
                category = None
            return dict(self.CATEGORY_CHOICES).get(category)
