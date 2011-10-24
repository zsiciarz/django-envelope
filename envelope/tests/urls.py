from django.conf.urls.defaults import include, patterns, url

from envelope.views import ContactView


urlpatterns = patterns('',
    (r'', include('envelope.urls')),
    url(r'^class_contact/', ContactView.as_view(), name='class_contact'),

    url(r'^customized_class_contact/',
        ContactView.as_view(
            success_url='customized_class_contact',
            template_name='contact.html'
        ),
        name='customized_class_contact'
    ),
)
