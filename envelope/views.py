# -*- coding: utf-8 -*-

u"""
The envelope contactform view.
"""

import logging
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from honeypot.decorators import check_honeypot
from envelope.forms import ContactForm


# global app logger
logger = logging.getLogger('envelope')

@check_honeypot
def contact(request, 
            form_class=ContactForm,
            template_name='envelope/contact.html',
            extra_context=None):
    u"""
    Contact form view.
    """
    if extra_context is None:
        extra_context = {}
    if request.method == 'POST':
        form = form_class(request.POST)
        #pylint: disable=E1101,E1103
        if form.is_valid():
            form.send()
            thank_you_message = getattr(settings, 'ENVELOPE_MESSAGE_THANKS',
                                        u"Thank you for your message.")
            messages.info(request, thank_you_message)
            return HttpResponseRedirect(reverse('envelope-contact'))
        else:
            error_message = getattr(settings, 'ENVELOPE_MESSAGE_ERROR',
                                    u"There was en error in the contact form.")
            messages.error(request, error_message)
        #pylint: enable=E1101,E1103
    else:
        if request.user.is_authenticated():
            initial = {
                'sender': '%s (%s)' % (request.user.username,
                                       request.user.get_full_name()),
                'email': request.user.email,
            }
            form = form_class(initial=initial)
        else:
            form = form_class()
    dictionary = {'form': form}
    for key, value in extra_context.items():
        dictionary[key] = callable(value) and value() or value
    return render_to_response(template_name,
                              dictionary,
                              context_instance=RequestContext(request))
