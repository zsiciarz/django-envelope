try:
    # Django 1.6+
    from django.conf.urls import patterns, include
except ImportError:
    # Django 1.4 and 1.5
    from django.conf.urls.defaults import patterns, include

urlpatterns = patterns('',
    (r'', include('envelope.urls')),
)
