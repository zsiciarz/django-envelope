# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Unit tests for ``django-envelope`` template tags.
"""

from django.test import TestCase
from django.template import TemplateSyntaxError

from envelope.templatetags.envelope_tags import render_contact_form


class RenderContactFormTestCase(TestCase):
    def test_no_form_in_context(self):
        """
        {% render_contact_form %} raises a syntax error when there is no form
        in the context.
        """
        context = {}
        with self.assertRaises(TemplateSyntaxError):
            render_contact_form(context)
