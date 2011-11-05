# -*- coding: utf-8 -*-

u"""
Views used to process the contact form.
"""

import logging

from django.contrib import messages
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView

from envelope import signals
from envelope.forms import ContactForm


logger = logging.getLogger('envelope.views')


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
            # the user might not have a full name, depends on the registration
            if user.get_full_name():
                sender = '%s (%s)' % (user.username, user.get_full_name())
            else:
                sender = user.username
            initial.update({
                'sender': sender,
                'email': user.email,
            })
        return initial

    def form_valid(self, form):
        u"""
        Sends the message and redirects the user somewhere.
        """
        responses = signals.before_send.send(sender=self.__class__,
                                             request=self.request,
                                             form=form)
        for (receiver, response) in responses:
            if not response:
                return HttpResponseBadRequest(_("Rejected by %s") %
                                                receiver.__name__)
        form.save()
        messages.info(self.request,
                      _("Thank you for your message."),
                      fail_silently=True)
        return redirect(self.get_success_url())

    def form_invalid(self, form):
        u"""
        When the form has errors, display it again.
        """
        messages.error(self.request,
                       _("There was en error in the contact form."),
                       fail_silently=True)
        return self.render_to_response(self.get_context_data(form=form))


def filter_spam(sender, request, form, **kwargs):
    u"""
    Handle spam filtering.
    """
    from envelope.spam_filters import check_honeypot
    return check_honeypot(request, form)


signals.before_send.connect(filter_spam, sender=ContactView,
                            dispatch_uid='envelope.views.filter_spam')
