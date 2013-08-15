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


@register.inclusion_tag('envelope/contact_form.html', takes_context=True)
def render_contact_form(context):
    """
    Renders the contact form which must be in the template context.
    """
    form = context['form']
    return {
        'form': form,
    }


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
