try:
    # Django 1.6+
    from django.conf.urls import patterns, include, url
except ImportError:
    # Django 1.5
    from django.conf.urls.defaults import patterns, include, url

from envelope.views import ContactView

urlpatterns = patterns('',
    url(r'', include('envelope.urls')),
    url(r'^crispy/', ContactView.as_view(template_name='envelope/crispy_contact.html'), name='crispy-contact'),
)
