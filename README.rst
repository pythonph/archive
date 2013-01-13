.. 

django-mango
======================

.. image:: https://travis-ci.org/pypug/django-mango.png
        :target: https://travis-ci.org/pypug/django-mango

More Mango, less Django!

Quickstart
----------

To bootstrap the project::

    virtualenv djangomango
    source djangomango/bin/activate
    cd path/to/djangomango/repository
    pip install -r requirements.pip
    pip install -e .
    cp djangomango/settings/local.py.example djangomango/settings/local.py
    manage.py syncdb --migrate

Documentation
-------------

Developer documentation is available in Sphinx format in the docs directory.

Initial installation instructions (including how to build the documentation as
HTML) can be found in docs/install.rst.

Notes
-----

This project is generated based on lincoln loop's Django Best Practices.
http://lincolnloop.com/django-best-practices/index.html
