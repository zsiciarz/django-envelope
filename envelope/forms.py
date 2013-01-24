# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Contact form class definitions.
"""

import logging
from smtplib import SMTPException

from django import forms
from django.core import mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from envelope import settings
from envelope.signals import after_send


logger = logging.getLogger('envelope.forms')


class BaseContactForm(forms.Form):
    """
    Base contact form class.

    The following form attributes can be overridden when creating the
    form or in a subclass. If you need more flexibility, you can instead
    override the associated methods such as `get_from_email()` (see below).

    ``subject_intro``
        Prefix used to create the subject line. Default is
        ``settings.ENVELOPE_SUBJECT_INTRO``.

    ``from_email``
        Used in the email from. Defaults to
        ``settings.ENVELOPE_FROM_EMAIL``.

    ``email_recipients``
        List of email addresses to send the email to. Defaults to
        ``settings.ENVELOPE_EMAIL_RECIPIENTS``.

    ``template_name``
        Template used to render the email message. Defaults to
        ``envelope/email_body.txt``.

    """
    sender = forms.CharField(label=_("From"), max_length=70)
    email = forms.EmailField(label=_("Email"))
    subject = forms.CharField(label=_("Subject"), max_length=127)
    message = forms.CharField(label=_("Message"), max_length=1000,
                              widget=forms.Textarea())

    subject_intro = settings.SUBJECT_INTRO
    from_email = settings.FROM_EMAIL
    email_recipients = settings.EMAIL_RECIPIENTS
    template_name = 'envelope/email_body.txt'

    def __init__(self, *args, **kwargs):
        for kwarg in list(kwargs):
            if hasattr(self, kwarg):
                setattr(self, kwarg, kwargs.pop(kwarg))
        super(BaseContactForm, self).__init__(*args, **kwargs)

    def save(self):
        """
        Sends the message.
        """
        subject = self.get_subject()
        from_email = self.get_from_email()
        email_recipients = self.get_email_recipients()
        context = self.get_context()
        message_body = render_to_string(self.get_template_names(), context)
        try:
            message = mail.EmailMessage(
                subject=subject,
                body=message_body,
                from_email=from_email,
                to=email_recipients,
                headers={
                    'Reply-To': self.cleaned_data['email']
                }
            )
            message.send()
            after_send.send(sender=self.__class__, message=message, form=self)
            logger.info(_("Contact form submitted and sent (from: %s)") %
                        self.cleaned_data['email'])
        except SMTPException:
            logger.exception(_("An error occured while sending the email"))
            return False
        else:
            return True

    def get_context(self):
        """
        Returns context dictionary for the email body template.

        By default, the template has access to all form fields' values
        stored in ``self.cleaned_data``. Override this method to set
        additional template variables.
        """
        return self.cleaned_data.copy()

    def get_subject(self):
        """
        Returns a string to be used as the email subject.

        Override this method to customize the display of the subject.
        """
        return self.subject_intro + self.cleaned_data['subject']

    def get_from_email(self):
        """
        Returns the from email address.

        Override to customize how the from email address is determined.
        """
        return self.from_email

    def get_email_recipients(self):
        """
        Returns a list of recipients for the message.

        Override to customize how the email recipients are determined.
        """
        return self.email_recipients

    def get_template_names(self):
        """
        Returns a template_name (or list of template_names) to be used
        for the email message.

        Override to use your own method choosing a template name.
        """
        return self.template_name


class ContactForm(BaseContactForm):
    """
    The default contact form class.

    This class extends the base form with a possibility to select
    message category. For example, user can ask a general question
    regarding the website or a more specific one, like "ask tech
    support" or "I want to speak to the manager".

    The categories are controlled by configuring
    ``ENVELOPE_CONTACT_CHOICES`` in your settings.py. The value for this
    setting should be a tuple of 2-element tuples, as usual with Django
    choice fields. Keep first elements of those tuples as integer values
    (or use None for the category "Other").

    You can additionally override ``category_choices`` or
    ``get_category_choices()`` in a subclass.
    """
    category_choices = settings.CONTACT_CHOICES
    category = forms.ChoiceField(label=_("Category"), choices=category_choices)

    def __init__(self, *args, **kwargs):
        """
        Category choice will be rendered above the subject field.
        """
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'sender',
            'email',
            'category',
            'subject',
            'message',
        ]
        self.fields['category'].choices = self.get_category_choices()

    def get_context(self):
        """
        Adds full category description to template variables in order
        to display the category in email body.
        """
        context = super(ContactForm, self).get_context()
        context['category'] = self.get_category_display()
        return context

    def get_category_choices(self):
        """
        Returns a tuple of 2-element category tuples.

        Override this method to customize the generation of categories.
        """
        return self.category_choices

    def get_category_display(self):
        """
        Returns the displayed name of the selected category.
        """
        try:
            category = int(self.cleaned_data['category'])
        except (AttributeError, ValueError, KeyError):
            category = None
        return dict(self.get_category_choices()).get(category)
