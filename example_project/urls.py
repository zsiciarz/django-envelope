from __future__ import unicode_literals

try:
    # Django 1.6+
    from django.conf.urls import patterns, include, url
except ImportError:
    # Django 1.5
    from django.conf.urls.defaults import patterns, include, url


from braces.views import FormMessagesMixin

from envelope.views import ContactView


class MessagesContactView(FormMessagesMixin, ContactView):
    form_invalid_message = "There was en error in the contact form."
    form_valid_message = "Thank you for your message."
    template_name = "envelope/messages_contact.html"


urlpatterns = patterns('',
    url(r'', include('envelope.urls')),
    url(r'^crispy/', ContactView.as_view(template_name='envelope/crispy_contact.html'), name='crispy-contact'),
    url(r'^messages/', MessagesContactView.as_view(), name='messages-contact'),
)
