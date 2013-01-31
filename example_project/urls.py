from django.conf.urls import patterns

urlpatterns = patterns('',
    (r'', include('envelope.urls')),
)
