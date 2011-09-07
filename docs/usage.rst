=====
Usage
=====

Add ``envelope`` and ``honeypot`` to your ``INSTALLED_APPS`` in ``settings.py``. The application
does not define any models, so a ``manage.py syncdb`` is *not needed*. 

For a quick start, simply include the app's ``urls.py`` in your main URLconf, like
this::

    urlpatterns = patterns('',
        #...
        (r'^contact/',    include('envelope.urls')),
        #...
    )

That's basically it. Navigate to the given URL and see the contact form in
action. See :doc:`customization` for more customization options.

