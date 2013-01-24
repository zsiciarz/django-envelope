# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Unit tests for spam filters.
"""

from django.conf import settings
from django.test import TestCase
from django.utils import unittest

try:
    import honeypot
except ImportError:
    honeypot = None

from envelope.spam_filters import check_honeypot


# mocking form and request, no need to use the real things here
class FakeForm(object):
    pass


class FakeRequest(object):
    def __init__(self):
        self.method = 'POST'
        self.POST = {}


class CheckHoneypotTestCase(TestCase):
    """
    Unit tests for ``check_honeypot`` spam filter.
    """

    def setUp(self):

        self.form = FakeForm()
        self.request = FakeRequest()
        self.honeypot = getattr(settings, 'HONEYPOT_FIELD_NAME', 'email2')

    def test_empty_honeypot(self):
        """
        Empty honeypot field is a valid situation.
        """
        self.request.POST[self.honeypot] = ''
        self.assertTrue(check_honeypot(self.request, self.form))

    @unittest.skipIf(honeypot is None, "django-honeypot is not installed")
    def test_filled_honeypot(self):
        """
        A value in the honeypot field is an indicator of a bot request.
        """
        self.request.POST[self.honeypot] = 'Hi, this is a bot'
        self.assertFalse(check_honeypot(self.request, self.form))
