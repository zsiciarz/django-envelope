from __future__ import unicode_literals

from django.conf.urls import include, url

from braces.views import FormMessagesMixin

from envelope.views import ContactView


class MessagesContactView(FormMessagesMixin, ContactView):
    form_invalid_message = "There was en error in the contact form."
    form_valid_message = "Thank you for your message."
    template_name = "envelope/messages_contact.html"


urlpatterns = [
    url(r'', include('envelope.urls')),
    url(r'^crispy/', ContactView.as_view(template_name='envelope/crispy_contact.html'), name='crispy-contact'),
    url(r'^messages/', MessagesContactView.as_view(), name='messages-contact'),
]
