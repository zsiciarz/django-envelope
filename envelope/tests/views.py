u"""
Unit tests for ``django-envelope`` views.
"""


from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.utils.translation import ugettext_lazy as _


class ContactViewTestCase(TestCase):
    u"""
    Unit tests for ``envelope.views.contact`` view function.
    """

    def setUp(self):
        self.url = reverse('envelope-contact')
        self.customized_url = reverse('customized_contact')
        self.honeypot = getattr(settings, 'HONEYPOT_FIELD_NAME', 'email2')

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
        When an authenticated user hits the form view, his email is
        automatically filled in the email field.
        """
        user = User.objects.create_user('test', 'test@example.org', 'password')
        logged_in = self.client.login(username='test', password='password')
        self.assertTrue(logged_in)
        response = self.client.get(self.url)
        self.assertContains(response, 'value="test@example.org"')

    def test_honeypot(self):
        u"""
        If the honeypot field is not empty, keep the spammer off the page.
        """
        response = self.client.post(self.url, {self.honeypot: 'some value'})
        self.assertEqual(response.status_code, 400)
        response = self.client.post(self.url, {self.honeypot: ''})
        self.assertEqual(response.status_code, 200)

    def test_form_successful(self):
        u"""
        If the data is correct, a message is sent and the user is redirected.
        """
        response = self.client.post(self.url, {
            'sender':   'zbyszek',
            'email':    'test@example.com',
            'category': 10,
            'subject':  'A subject',
            'message':  'Hello there!',
            self.honeypot: '',
        }, follow=True)
        self.assertRedirects(response, self.url)
        self.assertEquals(len(response.redirect_chain), 1)
        flash_error_message = _("There was en error in the contact form.")
        self.assertNotContains(response, flash_error_message)
        flash_success_message = _("Thank you for your message.")
        self.assertContains(response, flash_success_message)

    def test_extra_context(self):
        u"""
        Custom context variables can be supplied to the view.
        """
        response = self.client.get(self.customized_url)
        self.assertIn('foo', response.context)
        self.assertEqual(response.context['foo'], 'bar')
        # evaluate callables
        self.assertIn('spam', response.context)
        self.assertEqual(response.context['spam'], 'eggs')

