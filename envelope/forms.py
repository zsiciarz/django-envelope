# -*- coding: utf-8 -*-

u"""
Envelope contact form.
"""

import logging
from smtplib import SMTPException
from django import forms
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


# globalny logger dla aplikacji
logger = logging.getLogger('envelope')

DEFAULT_CONTACT_CHOICES = (
    ('',    u"Choose"),
    (10,    u"A general question regarding the website"),
    (None,   u"Other"),
)
CONTACT_CHOICES = getattr(settings, 'ENVELOPE_CONTACT_CHOICES',
                          DEFAULT_CONTACT_CHOICES)

#pylint: disable=W0232,E1101
class ContactForm(forms.Form):
    u"""
    Default contact form class.
    """
    sender = forms.CharField(label=u"From",
                             max_length=70)
    email = forms.EmailField(label=u"Email")
    category = forms.ChoiceField(label=u"Category",
                                 choices=CONTACT_CHOICES)
    subject = forms.CharField(label=u"Subject",
                              max_length=127)
    message = forms.CharField(label=u"Message", 
                              max_length=1000, 
                              widget=forms.Textarea())

    def send(self):
        u"""
        Sends the message.
        """
        subject_intro = getattr(settings, 'ENVELOPE_SUBJECT_INTRO',
                                u"Message from contact form: ")
        subject = subject_intro + self.cleaned_data['subject']
        dictionary = self.cleaned_data.copy()
        dictionary['category'] = self.get_category_display() 
        message = render_to_string('envelope/email_body.txt', dictionary)
        from_email = settings.DEFAULT_FROM_EMAIL
        to_email = [settings.DEFAULT_FROM_EMAIL]
        try:
            send_mail(subject, message, from_email, to_email)
            logger.info(u"Contact form submitted and sent (from: %s)" % self.cleaned_data['email'])
        except SMTPException, e:
            logger.error(u"Contact form error (%s)" % e)

    def get_category_display(self):
        u"""
        Returns the name of the selected category.
        """
        try:
            category = int(self.cleaned_data['category'])
        except ValueError:
            category = None
        return dict(CONTACT_CHOICES).get(category)
