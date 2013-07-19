# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Unit tests for ``django-envelope`` forms.
"""

from smtplib import SMTPException

from django.core import mail
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _

from mock import patch

from envelope.forms import BaseContactForm, ContactForm


class BaseContactFormTestCase(TestCase):
    """
    Unit tests for ``BaseContactForm`` class.
    """

    def setUp(self):
        self.form_data = {
            'sender': 'me',
            'email': 'test@example.com',
            'subject': 'A subject',
            'message': 'Hello there!',
        }

    def test_sender_field(self):
        """
        Sender field is required.
        """
        self._test_required_field('sender')

    def test_email_field(self):
        """
        E-mail field is required.
        """
        self._test_required_field('email')

    def test_subject_field(self):
        """
        Subject field is required.
        """
        self._test_required_field('subject')

    def test_message_field(self):
        """
        Message field is required.
        """
        self._test_required_field('message')

    def test_all_fields_valid(self):
        """
        When all required fields are supplied, the form is valid.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_get_context(self):
        """
        get_context() returns a copy of form's cleaned_data.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        context = form.get_context()
        self.assertEqual(context, form.cleaned_data)
        self.assertFalse(context is form.cleaned_data)

    def test_save(self):
        """
        A call to save() on a valid form sends the message.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        result = form.save()
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.form_data['subject'], mail.outbox[0].subject)

    def test_init_attr_override(self):
        """
        Attributes can be overridden on __init__()
        """
        overrides = {
            'subject_intro': 'New subject style: ',
            'from_email': 'new@example.com',
            'email_recipients': ['new_to@example.com'],
        }
        form = BaseContactForm(self.form_data, **overrides)
        form.is_valid()
        form.save()
        self.assertIn(overrides['subject_intro'], mail.outbox[0].subject)
        self.assertIn(overrides['from_email'], mail.outbox[0].from_email)
        self.assertIn(overrides['email_recipients'][0], mail.outbox[0].recipients())

    def test_save_smtp_error(self):
        """
        If the email backend raised an error, the message is not sent.
        """
        form = BaseContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        with patch.object(mail.EmailMessage, 'send', side_effect=SMTPException):
            result = form.save()
            self.assertFalse(result)
            self.assertEqual(len(mail.outbox), 0)

    def _test_required_field(self, field_name):
        """
        Check that the form does not validate without a given field.
        """
        del self.form_data[field_name]
        form = BaseContactForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(field_name, form.errors)


class ContactFormTestCase(TestCase):
    """
    Unit tests for ``ContactForm`` class.
    """

    def setUp(self):
        self.form_data = {
            'sender': 'me',
            'email': 'test@example.com',
            'category': 10,
            'subject': 'A subject',
            'message': 'Hello there!',
        }

    def test_category_field(self):
        """
        Message field is required.
        """
        del self.form_data['category']
        form = ContactForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)

    def test_get_context(self):
        """
        get_context() is overridden and adds a 'category' variable.
        """
        form = ContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        context = form.get_context()
        self.assertIn('category', context)

    def test_get_category_display(self):
        """
        A non-integer field value selects a category labeled "Other".
        """
        self.form_data['category'] = 'not-an-integer'
        form = ContactForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.get_category_display(), _("Other"))
