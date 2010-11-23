# -*- coding: utf-8 -*-

u"""
The envelope contactform view.
"""

import logging
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.translation import ugettext as _
from honeypot.decorators import check_honeypot
from envelope.forms import ContactForm


# global app logger
logger = logging.getLogger('envelope')

@check_honeypot
def contact(request, 
            form_class=ContactForm,
            template_name='envelope/contact.html',
            redirect_to=None,
            extra_context=None):
    u"""
    Contact form view.
    
    If the user is authenticated, ``sender`` and ``email`` fields are 
    automatically filled with proper values.
    
    **Optional arguments:**
        * ``form_class``: Which form class to use for contact message handling.
          The default (``ContactForm``) is often enough, but you can subclass
          it if you want, or even replace with a totally custom class. The
          only requirement is that your custom class has a ``save()``
          method which should send the message somewhere. Stick to the default,
          or its subclasses.
        * ``template_name``: Full name of the template which will display
          the form. By default it is "envelope/contact.html".
        * ``redirect_to``: URL of the page with some kind of a "thank you
          for your feedback", displayed after the form is successfully
          submitted. If left unset, the view redirects to itself.
        * ``extra_context``: A dictionary of values to add to template context.
    """
    if extra_context is None:
        extra_context = {}
    if request.method == 'POST':
        form = form_class(request.POST)
        #pylint: disable=E1101,E1103
        if form.is_valid():
            form.save()
            messages.info(request, _("Thank you for your message."), fail_silently=True)
            if redirect_to is None:
                redirect_to = reverse('envelope.views.contact')
            return HttpResponseRedirect(redirect_to)
        else:
            messages.error(request, _("There was en error in the contact form."), fail_silently=True)
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
