# -*- coding: utf-8 -*-

u"""
Envelope contact form.
"""

import logging
from smtplib import SMTPException

from django import forms
from django.core import mail
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from envelope import settings


logger = logging.getLogger('envelope.forms')


class BaseContactForm(forms.Form):
    u"""
    Base contact form class.
    """
    sender = forms.CharField(label=_("From"), max_length=70)
    email = forms.EmailField(label=_("Email"))
    subject = forms.CharField(label=_("Subject"), max_length=127)
    message = forms.CharField(label=_("Message"), max_length=1000,
                              widget=forms.Textarea())

    def save(self):
        u"""
        Sends the message.
        """
        subject = settings.ENVELOPE_SUBJECT_INTRO + self.cleaned_data['subject']
        context = self.get_context()
        message = render_to_string('envelope/email_body.txt', context)
        try:
            mail.send_mail(subject, message, settings.ENVELOPE_FROM_EMAIL,
                           settings.ENVELOPE_EMAIL_RECIPIENTS)
            logger.info(_("Contact form submitted and sent (from: %s)") %
                        self.cleaned_data['email'])
        except SMTPException:
            logger.exception(_("An error occured while sending the email"))
            return False
        else:
            return True

    def get_context(self):
        u"""
        Returns a dictionary of values to be passed to the email body template.

        Override this method to set additional template variables.
        """
        return self.cleaned_data.copy()


class ContactForm(BaseContactForm):
    u"""
    The default contact form class.

    This class extends the base form with a possibility to select message
    category. For example, user can ask a general question regarding the
    website or a more specific one, like "ask tech support" or "I want to speak
    to the manager".

    The categories are controlled by configuring ``ENVELOPE_CONTACT_CHOICES`` in
    your settings.py. The value for this setting should be a tuple of 2-element
    tuples, as usual with Django choice fields. Keep first elements of those
    tuples as integer values (or use None for the category "Other").
    """
    category = forms.ChoiceField(label=_("Category"),
                                 choices=settings.ENVELOPE_CONTACT_CHOICES)

    def __init__(self, *args, **kwargs):
        u"""
        This does the trick with placing category choice above the subject.
        """
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields.keyOrder = [
            'sender',
            'email',
            'category',
            'subject',
            'message',
        ]

    def get_context(self):
        u"""
        Adds full category description to template variables in order to display
        the category in email body.
        """
        context = super(ContactForm, self).get_context()
        context['category'] = self.get_category_display()
        return context

    def get_category_display(self):
        u"""
        Returns the displayed name of the selected category.
        """
        try:
            category = int(self.cleaned_data['category'])
        except (AttributeError, ValueError):
            category = None
        return dict(settings.ENVELOPE_CONTACT_CHOICES).get(category)
