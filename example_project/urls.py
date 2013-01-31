try:
	# Django 1.5 and below.
    from django.conf.urls.defaults import patterns, url
except ImportError:
	# Django 1.6+
    from django.conf.urls import patterns, url

urlpatterns = patterns('',
    (r'', include('envelope.urls')),
)
