from django.conf.urls import include, url

from envelope.views import ContactView


class SubclassedContactView(ContactView):
    pass


urlpatterns = [
    url(r'', include('envelope.urls')),
    url(r'^class_contact/', ContactView.as_view(), name='class_contact'),

    url(r'^customized_class_contact/',
        ContactView.as_view(
            success_url='customized_class_contact',
            template_name='customized_contact.html'
        ),
        name='customized_class_contact'
    ),

    url(r'^subclassed_class_contact/',
        SubclassedContactView.as_view(),
        name='subclassed_class_contact'
    ),
]
