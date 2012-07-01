===========
Development
===========

Contributing
============

Report bugs
-----------

Use the `issue tracker`_ on GitHub to file bugs.

Hack on the code
----------------

Fork the repository on GitHub, do your work in your fork (rhymes, eh?)
and send me a pull request. Try to conform to :pep:`8` and make sure
the tests pass (see below).


Running tests
=============

.. note::
   It is recommended to work in a virtualenv_.

All dependencies required for running tests and building documentation are
specified in the file ``pip-requirements.txt``.

To get the tests up and running, follow these commands::

    virtualenv --no-site-packages envelope
    cd envelope
    source bin/activate
    git clone git://github.com/zsiciarz/django-envelope.git
    cd django-envelope
    python setup.py develop
    pip install -r pip-requirements.txt
    python runtests.py

.. note::
   First three steps can be simplified by using virtualenvwrapper_.

To get a coverage report, replace the last command with::

    coverage run runtests.py && coverage html


CI Server
=========

A `Jenkins instance`_ is running at `ShiningPanda`_.


.. _`issue tracker`: https://github.com/zsiciarz/django-envelope/issues
.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _`Jenkins instance`: https://jenkins.shiningpanda.com/django-envelope/
.. _`ShiningPanda`: https://www.shiningpanda.com/
