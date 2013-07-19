# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Unit tests for ``django-envelope`` views.
"""

import os

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.utils import override_settings
from django.utils import unittest
from django.utils.translation import ugettext_lazy as _

try:
    import honeypot
except ImportError:
    honeypot = None

from envelope import signals


test_templates = (
    os.path.join(os.path.dirname(__file__), 'templates'),
    os.path.join(os.path.dirname(__file__), '../templates'),
)


@override_settings(TEMPLATE_DIRS=test_templates)
class ContactViewTestCase(TestCase):
    """
    Unit tests for contact form view.
    """
    urls = 'envelope.tests.urls'

    def setUp(self):
        self.url = reverse('envelope-contact')
        self.customized_url = reverse('customized_class_contact')
        self.subclassed_url = reverse('subclassed_class_contact')
        self.honeypot = getattr(settings, 'HONEYPOT_FIELD_NAME', 'email2')
        self.form_data = {
            'sender': 'zbyszek',
            'email': 'test@example.com',
            'category': 10,
            'subject': 'A subject',
            'message': 'Hello there!',
            self.honeypot: '',
        }

    def test_response_data(self):
        """
        A GET request displays the contact form.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "envelope/contact.html")
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_prefilled_form(self):
        """
        When an authenticated user hits the form view, his username, full name
        and email address are automatically filled in.
        """
        user = User.objects.create_user('test', 'test@example.org', 'password')
        user.first_name = 'John'
        user.last_name = 'Doe'
        user.save()
        logged_in = self.client.login(username='test', password='password')
        self.assertTrue(logged_in)
        response = self.client.get(self.url)
        self.assertContains(response, 'value="test (John Doe)"')
        self.assertContains(response, 'value="test@example.org"')

        self.client.logout()
        response = self.client.get(self.url)
        self.assertNotContains(response, 'value="test (John Doe)"')
        self.assertNotContains(response, 'value="test@example.org"')

    def test_prefilled_form_no_full_name(self):
        """
        In case the user is authenticated, but doesn't have his first and last
        name set (depends on the registration process), only his username is
        prefilled in the "From" field.
        """
        User.objects.create_user('test', 'test@example.org', 'password')
        logged_in = self.client.login(username='test', password='password')
        self.assertTrue(logged_in)
        response = self.client.get(self.url)
        self.assertContains(response, 'value="test"')

    @unittest.skipIf(honeypot is None, "django-honeypot is not installed")
    def test_honeypot(self):
        """
        If the honeypot field is not empty, keep the spammer off the page.
        """
        self.form_data.update({self.honeypot: 'some value'})
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 400)
        self.form_data.update({self.honeypot: ''})
        response = self.client.post(self.url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_form_invalid(self):
        """
        If the POST data is incorrect, the form is invalid.
        """
        self.form_data.update({'sender': ''})
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 200)
        flash_error_message = _("There was en error in the contact form.")
        self.assertContains(response, flash_error_message)

    def test_form_successful(self):
        """
        If the data is correct, a message is sent and the user is redirected.
        """
        response = self.client.post(self.url, self.form_data, follow=True)
        self.assertRedirects(response, self.url)
        self.assertEqual(len(response.redirect_chain), 1)
        flash_error_message = _("There was en error in the contact form.")
        self.assertNotContains(response, flash_error_message)
        flash_success_message = _("Thank you for your message.")
        self.assertContains(response, flash_success_message)

    def test_signal_before_send(self):
        """
        A ``before_send`` signal is emitted before sending the message.
        """
        # ugly trick to access the variable from inner scope
        params = {}

        def handle_before_send(sender, request, form, **kwargs):
            params['form'] = form

        signals.before_send.connect(handle_before_send)
        self.client.post(self.url, self.form_data, follow=True)
        self.assertEqual(params['form'].cleaned_data['email'], self.form_data['email'])

    def test_signal_after_send(self):
        """
        An ``after_send`` signal is sent after succesfully sending the message.
        """
        params = {}

        def handle_after_send(sender, message, form, **kwargs):
            params['message'] = message

        signals.after_send.connect(handle_after_send)
        self.client.post(self.url, self.form_data, follow=True)
        self.assertIn(self.form_data['subject'], params['message'].subject)

    def test_custom_template(self):
        """
        You can change the default template used to render the form.
        """
        response = self.client.get(self.customized_url)
        self.assertTemplateUsed(response, "contact.html")

    def test_custom_success_url(self):
        """
        The view redirects to a custom success_url when the form is valid.
        """
        response = self.client.post(self.customized_url, self.form_data)
        self.assertRedirects(response, self.customized_url)

    def test_issue_18(self):
        """
        ContactView subclasses should also trigger spam filtering.

        See: https://github.com/zsiciarz/django-envelope/issues/18
        """
        self.form_data.update({self.honeypot: 'some value'})
        response = self.client.post(self.subclassed_url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 400)
