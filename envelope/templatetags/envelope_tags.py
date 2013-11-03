# -*- coding: utf-8 -*-

from __future__ import unicode_literals

"""
Template tags related to the contact form.
"""

from django import template

try:
    import honeypot
except ImportError:  # pragma: no cover
    honeypot = None


register = template.Library()


@register.inclusion_tag('envelope/contact_form.html', takes_context=True)
def render_contact_form(context):
    """
    Renders the contact form which must be in the template context.

    The most common use case for this template tag is to call it in the
    template rendered by :class:`~envelope.views.ContactView`. The template
    tag will then render a sub-template ``envelope/contact_form.html``.

    .. versionadded:: 0.7.0
    """
    try:
        form = context['form']
    except KeyError:
        raise template.TemplateSyntaxError("There is no 'form' variable in the template context.")
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
