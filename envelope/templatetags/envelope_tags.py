# -*- coding: utf-8 -*-
"""
Template tags related to the contact form.
"""

from __future__ import unicode_literals

from django import template

register = template.Library()

try:
    import honeypot

    # Register antispam_fields as an inclusion tag
    t = template.Template('{% load honeypot %}{% render_honeypot_field %}')
    register.inclusion_tag(t, name='antispam_fields')(lambda: {})

except ImportError:  # pragma: no cover
    # Register antispam_fields as an empty tag
    register.simple_tag(name='antispam_fields')(lambda: '')


@register.inclusion_tag('envelope/contact_form.html', takes_context=True)
def render_contact_form(context):
    """
    Renders the contact form which must be in the template context.

    The most common use case for this template tag is to call it in the
    template rendered by :class:`~envelope.views.ContactView`. The template
    tag will then render a sub-template ``envelope/contact_form.html``.
    """
    if 'form' not in context:
        raise template.TemplateSyntaxError(
            "There is no 'form' variable in the template context."
        )
    return context
