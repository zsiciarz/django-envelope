u"""
Unit tests for ``django-envelope`` forms.
"""

import warnings
from smtplib import SMTPException

from django.conf import settings
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from envelope.forms import BaseContactForm, ContactForm


class BaseContactFormTestCase(TestCase):
    u"""
    Unit tests for ``BaseContactForm`` class.
    """

    def setUp(self):
        self.form_data = {
            'sender':   'me',
            'email':    'test@example.com',
            'subject':  'A subject',
            'message':  'Hello there!'
        }

    def test_sender_field(self):
        u"""
        Sender field is required.
        """
        self._test_required_field('sender')

    def test_email_field(self):
        u"""
        E-mail field is required.
        """
        self._test_required_field('email')

    def test_subject_field(self):
        u"""
        Subject field is required.
        """
        self._test_required_field('subject')

    def test_message_field(self):
        u"""
        Message field is required.
        """
        self._test_required_field('message')

    def test_all_fields_valid(self):
        u"""
        When all required fields are supplied, the form is valid.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_get_context(self):
        u"""
        get_context() returns a copy of form's cleaned_data.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        context = form.get_context()
        self.assertEqual(context, form.cleaned_data)
        self.assertFalse(context is form.cleaned_data)

    def test_save(self):
        u"""
        A call to save() on a valid form sends the message.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        result = form.save()
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.form_data['subject'], mail.outbox[0].subject)

    def test_save_smtp_error(self):
        u"""
        If the email backend raised an error, the message is not sent.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        old_send_mail = mail.send_mail
        def new_send_mail(*args):
            raise SMTPException
        try:
            mail.send_mail = new_send_mail
            result = form.save()
            self.assertFalse(result)
            self.assertEqual(len(mail.outbox), 0)
        finally:
            mail.send_mail = old_send_mail

    def test_send(self):
        u"""
        send() is deprecated, but still sends the message.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        with warnings.catch_warnings(record=True) as warns:
            warnings.filterwarnings("always", category=DeprecationWarning)
            result = form.send()
            self.assertEqual(len(warns), 1)
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.form_data['subject'], mail.outbox[0].subject)

    def _test_required_field(self, field_name):
        del self.form_data[field_name]
        form = BaseContactForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(field_name, form.errors)


class ContactFormTestCase(TestCase):
    u"""
    Unit tests for ``ContactForm`` class.
    """

    def setUp(self):
        self.form_data = {
            'sender':   'me',
            'email':    'test@example.com',
            'category': 10,
            'subject':  'A subject',
            'message':  'Hello there!'
        }

    def test_category_field(self):
        u"""
        Message field is required.
        """
        del self.form_data['category']
        form = ContactForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_get_context(self):
        u"""
        get_context() is overridden and adds a 'category' variable.
        """
        form = ContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        context = form.get_context()
        self.assertIn('category', context)

    def test_get_category_display(self):
        u"""
        A non-integer field value selects a category labeled "Other".
        """
        self.form_data['category'] = 'not-an-integer'
        form = ContactForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.get_category_display(), _("Other"))

