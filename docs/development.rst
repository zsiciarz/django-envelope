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

All dependencies required for running tests are specified in the file
``test_requirements.txt``.

.. note::
   If you get errors such as ``ImportError: No module named mock`` while
   running tests, you're probably on Python 2 (Python 3 has ``mock`` in
   standard library). To fix that, run ``pip install mock``.

To get the tests up and running, follow these commands::

    virtualenv envelope
    cd envelope
    source bin/activate
    git clone https://github.com/zsiciarz/django-envelope.git
    cd django-envelope
    pip install -r test_requirements.txt
    make test

.. note::
   First three steps can be simplified by using virtualenvwrapper_.

To get a coverage report, replace the last command with::

    make coverage


CI Server
=========

The GitHub repository is hooked to `Travis CI`_. Travis worker pushes code
coverage to `coveralls.io`_ after each successful build.


.. _`issue tracker`: https://github.com/zsiciarz/django-envelope/issues
.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _`Travis CI`: https://travis-ci.org/zsiciarz/django-envelope
.. _`coveralls.io`: https://coveralls.io/r/zsiciarz/django-envelope
