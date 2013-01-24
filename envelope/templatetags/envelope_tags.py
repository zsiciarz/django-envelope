# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Templatetags related to the contact form.
"""

from django import template

try:
    import honeypot
except ImportError:
    honeypot = None


register = template.Library()


@register.simple_tag
def antispam_fields():
    """
    Returns the HTML for any spam filters available.
    """
    content = ''
    if honeypot:
        t = template.Template('{% load honeypot %}{% render_honeypot_field %}')
        content += t.render(template.Context({}))
    return content
