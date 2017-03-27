==================
 Django Spectator
==================

.. image:: https://travis-ci.org/philgyford/django-spectator.svg?branch=master
  :target: https://travis-ci.org/philgyford/django-spectator?branch=master

.. image:: https://coveralls.io/repos/github/philgyford/django-spectator/badge.svg?branch=master
  :target: https://coveralls.io/github/philgyford/django-spectator?branch=master

A Django app to track book reading, movie viewing, gig going and play watching.

v1.0 STILL IN PROGRESS.

So far only used with Python 3.6 and Django 1.10. Should work with Python
3.5+ and Django 1.8+.

It has URLs, views and templates to create a site displaying all the data, and
Django admin screens to add and edit them. The templates use `Bootstrap v4-alpha.6 <https://v4-alpha.getbootstrap.com>`_.

There are also template tags for displaying data in your own templates (see
below).


************
Installation
************

Install with pip (not working yet)::

    pip install django-spectator

Add it and django-polymorphic to your project's ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = [
        ...
        'polymorphic',
        'spectator',
    ]

Run migrations::

    ./manage.py makemigrations

Optionally get a `Google Maps JavaScript API key <https://developers.google.com/maps/documentation/javascript/get-api-key>`_ and add it to your ``settings.py`` like this::

    SPECTATOR_GOOGLE_MAPS_API_KEY = 'YOUR-API-KEY'

This will enable using a map in the Django Admin to set the location of Venues,
and the displaying of Venues' maps in the public templates.

Then, go to Django Admin to add your data.


********
Overview
********

There are two main parts to Spectator: Reading and Events (movies, concerts, etc).

Creators
========

Reading and Events both share Creators, which are the authors of books, directors of movies, actors in plays, groups who perfom at gigs, etc.

A Creator has a name and a ``kind``, of either "individual" (e.g. "Anthony Sher") or "group" (e.g. "Royal Shakespeare Company").

A Creator is associated with books, movies, concerts, etc. through roles, which
include an optional ``role_name`` such as "Author", "Illustrator", "Director",
"Playwright", "Company", etc. The roles can be given an order so that the
creators of a thing will be listed in the appropriate order (such as the
director before a movie's actors).

See ``spectator/models/core.py`` for these models.

Reading
=======

A Publication is a thing that's been read, and has a ``kind`` of either "book"
or "periodical". A Publication can optionally be part of a PublicationSeries.
e.g. a Publication "Vol. 3 No. 7 September 2005" could be part of the "The
Believer" PublicationSeries.

A Publication can have zero or more Readings. A Reading can have
a ``start_date`` and ``end_date``. If the ``start_date`` is set but the
``end_date`` isn't, the Publication is currently being read. When a Reading has
been completed, and an ``end_date`` added, it can be marked as ``is_finished``
or not. If not, it's because you gave up on the Publication before getting to
the end.

Both ``start_date`` and ``end_date`` indicates a specific day by default. If
you don't know the day, or the month, a granularity can be specified indicating
whether the reading started/ended sometime during the month or year.

See ``spectator/models/reading.py`` for these models.

Events
======

An Event specifies a date on which you saw a thing at a particular Venue.
A Venue has a name and, optionally, location details.

The different kinds of Events have different structures:

Concerts and MiscEvents
-----------------------

A Concert, and the generic MiscEvents, are the simplest. A date when you
went to a Venue to see one or more Creators. The Concert/MiscEvent can
optionally have a title.

Movies
------

A Movie is a film created by (optionally) one or more Creators. It can
optionally have a year and an IMDb ID.

A MovieEvent is when a particular Movie was seen on a specific date at a specific Venue.

Plays
-----

A Play (e.g. "King Lear") is created by zero or more Creators (e.g. "William
Shakespeare (Playwright)").

A PlayProduction is a particular production of that play by zero or more
Creators. For example, one might be by "Royal Shakespeare Company" with
"Anthony Sher (King Lear)". Another might be by "Deborah Warner (Director)"
with "Glenda Jackson (King Lear)".

A PlayProductionEvent is when a particular PlayProduction was seen on
a specific date at a specific Venue.

When adding a new Play in the Django Admin, it's best to fill in the Play
details, click "Save and continue editing", then click "Add another Play Production and event" to add the details of the particular production and when it was seen.


*************
Template tags
*************

To use any of these tags in a template, first::

    {% load spectator_tags %}

In-progress Publications
========================

To get a QuerySet of Publications currently being read use
``in_progress_publications``::

    {% in_progress_publications as publications %}

    {% for pub in publications %}
        <p>{{ pub }}<br>
        {% for role in pub.roles.all %}
            {{ role.creator.name }}
            {% if role.role_name %}({{ role.role_name }}){% endif %}
            <br>
        {% endfor %}
        </p>
    {% endfor %}

Or to display as a Bootstrap card::

    {% in_progress_publications_card %}

Publications being read on a day
================================

To get a QuerySet of Publications that were being read on a particular day use
``day_publications``. If ``my_date`` is a python ``date`` object::

    {% day_publications date=my_date as publications %}

And display the results as in the above example.

Or to display as a Bootstrap card::

    {% day_publications_card date=my_date %}

Years of reading
================

To get a QuerySet of the years in which Publications were being read::

    {% reading_years as years %}

    {% for year in years %}
        {{ year|date:"Y" }}<br>
    {% endfor %}

Or to display as a Bootstrap card, with each year linking to the
``ReadingYearArchiveView``::

    {% reading_years_card current_year=year %}

Here, ``year`` is a date object indicating a year which shouldn't be linked.

Recent Events
=============

To get a QuerySet of Events that happened recently::

    {% recent_events num=3 as events %}

    {% for event in events %}
        <p>
            {{ event }}<br>
            {{ event.venue.name }}
        </p>
    {% endfor %}

If ``num`` is not specified, 10 are returned by default.

Or to display as a Boostrap card::

    {% recent_events_card num=3 %}

Events on a day
===============

To get a QuerySet of Events that happened on a particular day, use
``day_events``. If ``my_date`` is a python ``date`` object::

    {% day_events date=my_date as events %}

And display the results as in the above example.

Or to display as a Bootstrap card::

    {% day_events_card date=my_date %}

Years of Events
===============

To get a QuerySet of the years in which Events happened::

    {% events_years as years %}

    {% for year in years %}
        {{ year|date:"Y" }}<br>
    {% endfor %}

Or to display as a Bootstrap card, with each year linking to the
``EventYearArchiveView``::

    {% events_years_card current_year=year %}

Here, ``year`` is a date object indicating a year which shouldn't be linked.


*****************
Local development
*****************

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

Adding a new event type
-----------------------

* Add a child of the ``Event`` model, and a child of ``BaseRole`` for the through model and tests.
* Add factories for both event and role models.
* Add its admin.
* Add URLs and tests.
* Add Views and tests.
* Add count of objects in ``EventListView``.
* In ``events/event_list.html`` template, add tab.
* Add ``events/newtype_list.html`` and ``events/newtype_detail.html`` templates.
* Add to ``events/includes/event.html``.
* Add ``events/includes/newtype.html``.
* Add new type to ``core/creator_detail.html`` template.

``Concert`` and ``MiscEvent`` are almost identical at the moment. Scope for
refactoring?

