# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Unit tests for ``django-envelope`` forms.
"""

import unittest
from smtplib import SMTPException

from mock import patch

from envelope.forms import ContactForm


class ContactFormTestCase(unittest.TestCase):
    """
    Unit tests for ``ContactForm`` class.
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

    def test_message_field(self):
        """
        Message field is required.
        """
        self._test_required_field('message')

    def test_subject_field(self):
        """
        Subject field is optional.
        """
        del self.form_data['subject']
        form = ContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        self.assertNotIn('subject', form.errors)

    def test_all_fields_valid(self):
        """
        When all required fields are supplied, the form is valid.
        """
        form = ContactForm(self.form_data)
        self.assertTrue(form.is_valid())

    def test_get_context(self):
        """
        get_context() returns a copy of form's cleaned_data.
        """
        form = ContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        context = form.get_context()
        self.assertEqual(context, form.cleaned_data)
        self.assertIsNot(context, form.cleaned_data)

    def test_save(self):
        """
        A call to save() on a valid form sends the message.
        """
        form = ContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        with patch('django.core.mail.EmailMessage') as mock_message:
            mock_message.return_value.send.return_value = True
            result = form.save()
            self.assertTrue(result)
            args, kwargs = mock_message.call_args
            self.assertIn(self.form_data['subject'], kwargs['subject'])

    def test_init_attr_override(self):
        """
        Attributes can be overridden on __init__()
        """
        overrides = {
            'subject_intro': 'New subject style: ',
            'from_email': 'new@example.com',
            'email_recipients': ['new_to@example.com'],
        }
        form = ContactForm(self.form_data, **overrides)
        form.is_valid()
        with patch('django.core.mail.EmailMessage') as mock_message:
            mock_message.return_value.send.return_value = True
            form.save()
            args, kwargs = mock_message.call_args
            self.assertIn(overrides['subject_intro'], kwargs['subject'])
            self.assertIn(overrides['from_email'], kwargs['from_email'])
            self.assertIn(overrides['email_recipients'][0], kwargs['to'])

    def test_save_smtp_error(self):
        """
        If the email backend raised an error, the message is not sent.
        """
        form = ContactForm(self.form_data)
        self.assertTrue(form.is_valid())
        with patch('django.core.mail.EmailMessage') as mock_message:
            mock_message.return_value.send.side_effect = SMTPException
            result = form.save()
            self.assertFalse(result)

    def _test_required_field(self, field_name):
        """
        Check that the form does not validate without a given field.
        """
        del self.form_data[field_name]
        form = ContactForm(self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn(field_name, form.errors)
