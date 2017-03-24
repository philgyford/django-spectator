==================
 Django Spectator
==================

.. image:: https://travis-ci.org/philgyford/django-spectator.svg?branch=master
  :target: https://travis-ci.org/philgyford/django-spectator?branch=master

.. image:: https://coveralls.io/repos/github/philgyford/django-spectator/badge.svg?branch=master
  :target: https://coveralls.io/github/philgyford/django-spectator?branch=master

A Django app to track book reading, movie viewing, gig going and play watching.

So far only used with Python 3 and Django 1.10.

Very much a work in progress.

Local development
-----------------

``devproject/`` is a basic Django project to use the app locally. Use it like::

$ pip install -r devproject/requirements.txt
$ python setup.py develop
$ ./devproject/manage.py runserver

Run tests with tox. Install it with::

$ pip install tox

Run all tests in all environments like::

$ tox

To run tests in only one environment, specify it. In this case, Python 3.6 and Django 1.10::

$ tox -e py36-django110

To run a specific test, add its path after ``--``, eg::

$ tox -e py36-django110 -- tests.spectator.tests.test_models.CreatorTestCase.test_ordering

Running the tests in all environments will generate coverage output. There will also be an ``htmlcov/`` directory containing an HTML report. You can also generate these reports without running all the other tests::

$ tox -e coverage

### Adding a new event type

* Add a child of the `Event` model, and a child of `BaseRole` for the through model and tests.
* Add factories for both event and role models.
* Add its admin.
* Add URLs and tests.
* Add Views and tests.
* Add count of objects in `EventListView`.
* In `event_list.html` template, add tab.
* Add `newtype_list.html` and `newtype_detail.html` templates.
* Add to `includes/events.html`.
* Add `includes/newtype.html`.
* Add new type to `creator_detail.html` template.

`Concert` and `MiscEvent` are almost identical at the moment. Scope for
refactoring?

