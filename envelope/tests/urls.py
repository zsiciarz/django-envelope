from django.conf.urls.defaults import include, patterns, url

urlpatterns = patterns('',
    (r'', include('envelope.urls')),

    url(r'^customized_contact/',
        'envelope.views.contact',
        kwargs={
            'redirect_to': 'customized_contact',
            'extra_context': {
                'foo': 'bar',
                'spam': lambda: 'eggs',
            }
        },
        name='customized_contact'
    ),
)

