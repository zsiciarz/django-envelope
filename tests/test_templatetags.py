# -*- coding: utf-8 -*-
"""
Unit tests for ``django-envelope`` template tags.
"""

from __future__ import unicode_literals

from django.template import TemplateSyntaxError
from django.template.loader import render_to_string
from django.test import TestCase

from envelope.forms import ContactForm
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

    def test_antispamfield_not_escaped(self):
        """
        Antispam fields should not be escaped by Django.
        """
        context = {'form': ContactForm()}
        content = render_to_string('envelope/contact_form.html', context)
        self.assertNotIn('&lt;div', content)
