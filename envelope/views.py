# -*- coding: utf-8 -*-

u"""
Views used to process the contact form.
"""

import logging
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from honeypot.decorators import check_honeypot

from envelope.forms import ContactForm


# global app logger
logger = logging.getLogger('envelope')


class ContactView(FormView):
    u"""
    Contact form view (class-based).

    Displays the contact form upon a GET request. If the current user is
    authenticated, ``sender`` and ``email`` fields are automatically filled
    with proper values.

    When the form is submitted and valid, a message is sent and afterwards
    the user is redirected to a "thank you" page (by default it is the page
    with the form).

    ``form_class``
        Which form class to use for contact message handling.
        The default (:class:`envelope.forms.ContactForm`) is often enough,
        but you can subclass it if you want, or even replace with a totally
        custom class. The only requirement is that your custom class has a
        ``save()`` method which should send the message somewhere. Stick to
        the default, or its subclasses.

    ``template_name``
        Full name of the template which will display
        the form. By default it is "envelope/contact.html".

    ``success_url``
        URL of the page with some kind of a "thank you
        for your feedback", displayed after the form is successfully
        submitted. If left unset, the view redirects to itself.

    .. versionadded:: 0.3.0
    """
    form_class = ContactForm
    template_name = 'envelope/contact.html'
    success_url = None

    def get_success_url(self):
        u"""
        Returns the URL where the view will redirect after submission.
        """
        if self.success_url:
            return self.success_url
        else:
            return self.request.get_full_path()

    def get_initial(self):
        u"""
        Automatically fills form fields for authenticated users.
        """
        initial = super(ContactView, self).get_initial()
        user = self.request.user
        if user.is_authenticated():
            initial.update({
                'sender': '%s (%s)' % (user.username, user.get_full_name()),
                'email': user.email,
            })
        return initial

    def form_valid(self, form):
        u"""
        Sends the message and redirects the user somewhere.
        """
        form.save()
        messages.info(self.request, _("Thank you for your message."), fail_silently=True)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        u"""
        When the form has errors, display it again.
        """
        return self.render_to_response(self.get_context_data(form=form))

    @method_decorator(check_honeypot)
    def dispatch(self, *args, **kwargs):
        u"""
        Overridden here to make decorators work.
        """
        return super(ContactView, self).dispatch(*args, **kwargs)


@check_honeypot
def contact(request,
            form_class=ContactForm,
            template_name='envelope/contact.html',
            redirect_to=None,
            extra_context=None):
    u"""
    Contact form view (function-based).

    If the user is authenticated, ``sender`` and ``email`` fields are
    automatically filled with proper values.

    **Optional arguments:**
        * ``form_class``: Which form class to use for contact message handling.
          The default (:class:`envelope.forms.ContactForm`) is often enough,
          but you can subclass it if you want, or even replace with a totally
          custom class. The only requirement is that your custom class has a
          ``save()`` method which should send the message somewhere. Stick to
          the default, or its subclasses.
        * ``template_name``: Full name of the template which will display
          the form. By default it is "envelope/contact.html".
        * ``redirect_to``: URL of the page with some kind of a "thank you
          for your feedback", displayed after the form is successfully
          submitted. If left unset, the view redirects to itself.
        * ``extra_context``: A dictionary of values to add to template context.

    .. deprecated:: 0.3.0
    """
    import warnings
    warnings.warn("envelope.views.contact is deprecated, use the ContactView class instead", PendingDeprecationWarning)
    if extra_context is None:
        extra_context = {}
    if request.method == 'POST':
        form = form_class(request.POST)
        #pylint: disable=E1101,E1103
        if form.is_valid():
            form.save()
            messages.info(request, _("Thank you for your message."), fail_silently=True)
            if redirect_to is None:
                redirect_to = request.get_full_path()
            return redirect(redirect_to)
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

