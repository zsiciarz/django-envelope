u"""
Unit tests for ``django-envelope`` views.
"""

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _


class ContactViewTestCase(TestCase):
    u"""
    Unit tests for contact form view.
    """
    url = reverse('envelope-contact')
    customized_url = reverse('customized_class_contact')

    def setUp(self):
        self.honeypot = getattr(settings, 'HONEYPOT_FIELD_NAME', 'email2')
        self.form_data = {
            'sender':   'zbyszek',
            'email':    'test@example.com',
            'category': 10,
            'subject':  'A subject',
            'message':  'Hello there!',
            self.honeypot: '',
        }

    def test_response_data(self):
        u"""
        A GET request displays the contact form.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "envelope/contact.html")
        form = response.context['form']
        self.assertFalse(form.is_bound)

    def test_prefilled_form(self):
        u"""
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
        u"""
        In case the user is authenticated, but doesn't have his first and last
        name set (depends on the registration process), only his username is
        prefilled in the "From" field.
        """
        user = User.objects.create_user('test', 'test@example.org', 'password')
        logged_in = self.client.login(username='test', password='password')
        self.assertTrue(logged_in)
        response = self.client.get(self.url)
        self.assertContains(response, 'value="test"')

    def test_honeypot(self):
        u"""
        If the honeypot field is not empty, keep the spammer off the page.
        """
        self.form_data.update({self.honeypot: 'some value'})
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 400)
        self.form_data.update({self.honeypot: ''})
        response = self.client.post(self.url, self.form_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_form_invalid(self):
        u"""
        If the POST data is incorrect, the form is invalid.
        """
        self.form_data.update({'sender': ''})
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 200)
        flash_error_message = _("There was en error in the contact form.")
        self.assertContains(response, flash_error_message)

    def test_form_successful(self):
        u"""
        If the data is correct, a message is sent and the user is redirected.
        """
        response = self.client.post(self.url, self.form_data, follow=True)
        self.assertRedirects(response, self.url)
        self.assertEquals(len(response.redirect_chain), 1)
        flash_error_message = _("There was en error in the contact form.")
        self.assertNotContains(response, flash_error_message)
        flash_success_message = _("Thank you for your message.")
        self.assertContains(response, flash_success_message)

    def test_custom_template(self):
        u"""
        You can change the default template used to render the form.
        """
        response = self.client.get(self.customized_url)
        self.assertTemplateUsed(response, "contact.html")

    def test_custom_success_url(self):
        u"""
        The view redirects to a custom success_url when the form is valid.
        """
        response = self.client.post(self.customized_url, self.form_data)
        self.assertRedirects(response, self.customized_url)
