===============
django-envelope
===============

.. image:: https://img.shields.io/pypi/v/django-envelope.svg
    :target: https://pypi.python.org/pypi/django-envelope/
    :alt: Latest PyPI version

.. image:: https://img.shields.io/pypi/dm/django-envelope.svg
    :target: https://pypi.python.org/pypi/django-envelope/
    :alt: Number of PyPI downloads

.. image:: https://img.shields.io/pypi/pyversions/django-envelope.svg
    :target: https://pypi.python.org/pypi/django-envelope/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/wheel/django-envelope.svg
    :target: https://pypi.python.org/pypi/django-envelope/
    :alt: Wheel Status

.. image:: https://travis-ci.org/zsiciarz/django-envelope.png?branch=develop
    :target: https://travis-ci.org/zsiciarz/django-envelope

.. image:: https://coveralls.io/repos/zsiciarz/django-envelope/badge.png
    :target: https://coveralls.io/r/zsiciarz/django-envelope


``django-envelope`` is a simple contact form app for Django web framework.

Basic usage
-----------

1. Install with ``pip install django-envelope``.
2. Add ``envelope`` to your ``INSTALLED_APPS``.
3. Create a template ``envelope/contact.html`` that contains somewhere
   a call to ``{% render_contact_form %}`` template tag. This tag can be
   imported by placing ``{% load envelope_tags %}`` at the top of your
   template.
4. Hook the app's URLconf in your ``urls.py`` like this::

    urlpatterns = patterns('',
        #...
        (r'^contact/',    include('envelope.urls')),
        #...
    )

See the `docs <http://django-envelope.rtfd.org>`_ for more customization
options.

Resources
---------

 * `Documentation <http://django-envelope.rtfd.org>`_
 * `Issue tracker <https://github.com/zsiciarz/django-envelope/issues>`_
 * `CI server <https://travis-ci.org/zsiciarz/django-envelope>`_

Authors
-------

django-envelope was created by `Zbigniew Siciarz <http://siciarz.net>`_ and is
now maintained by `SebCorbin <https://github.com/SebCorbin>`_.
See AUTHORS.rst for a full list of contributors.

License
-------

This work is released under the MIT license. A copy of the license is provided
in the LICENSE file.

The HTML template comes from
`Open Source Template Project <https://github.com/sendwithus/templates>`_ by
sendwithus.com, distributed under the Apache 2.0 license (see the APACHE_LICENSE
file for the full text).
