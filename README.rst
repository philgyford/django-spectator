==================
 Django Spectator
==================

.. image:: https://travis-ci.org/philgyford/django-spectator.svg?branch=master
  :target: https://travis-ci.org/philgyford/django-spectator?branch=master

.. image:: https://coveralls.io/repos/github/philgyford/django-spectator/badge.svg?branch=master
  :target: https://coveralls.io/github/philgyford/django-spectator?branch=master

Two Django apps:

* One to track book and periodical reading, including start and end dates, authors.
* One to track events attended (movie, plays, gigs, exhibitions, comedy, dance,
  classical), including date, venue, and people/organisations involved.

For Django 1.11 or Django 2.0 running on Python 3.5 or 3.6.

It has URLs, views and templates to create a site displaying all the data, and
Django admin screens to add and edit them. The templates use `Bootstrap v4-beta <https://getbootstrap.com>`_.

There are also template tags for displaying data in your own templates (see
below).


************
Installation
************

Install with pip::

    pip install django-spectator

Add the apps to your project's ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = [
        ...
        'spectator.core',
        'spectator.events',
        'spectator.reading',
    ]

While ``spectator.core`` is required, you can omit either ``spectator.events``
or ``spectator.reading`` if you only want to use one of them.

Run migrations::

    ./manage.py migrate

Add to your project's ``urls.py``::

    urlpatterns = [
        # ...

        url(r'^spectator/', include('spectator.core.urls')),
    ]

You can change the initial path (``r'^spectator/'``) to whatever suits you. e.g.
use ``r'^'`` to have Spectator's home page be the front page of your site.

Then, go to Django Admin to add your data.


Settings
========

Optionally get a `Google Maps JavaScript API key <https://developers.google.com/maps/documentation/javascript/get-api-key>`_ and add it to your ``settings.py`` like this::

    SPECTATOR_GOOGLE_MAPS_API_KEY = 'YOUR-API-KEY'

This will enable using a map in the Django Admin to set the location of Venues,
and the displaying of Venues' maps in the public templates.

URLs for all objects include automatically-generated slugs, which are based on
[Hashids](http://hashids.org) of the object's ID. You can change which
characters are used in these slugs with this setting::

    SPECTATOR_SLUG_ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'

The default is ``'abcdefghijkmnopqrstuvwxyz23456789'``.

You can also change the salt value used to encode the slugs. While the slugs
don't provide complete security (i.e. it's not impossible to determine the ID on
which a slug is based), using your own salt value can't hurt::

    SPECTATOR_SLUG_SALT = 'My special salt value is here'

The default is ``'Django Spectator'``.


********
Overview
********

There are two main parts to Spectator: Reading and Events (movies, gigs, etc). They both share Creators.

Creators
========

Creators are the authors of books, directors of movies, actors in plays, groups who perfom at gigs, etc.

A Creator has a name and a ``kind``, of either "individual" (e.g. "Anthony Sher") or "group" (e.g. "Royal Shakespeare Company").

A Creator is associated with books, movies, events, etc. through roles, which
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

Each Event can have zero or more Creators associated directly with it. e.g. the
performers at a gig, the comedians at a comedy event. These can be in a spectific
order, and each with an optional role. e.g:

* The Wedding Present
    * Role: Headliner
    * Order: 1
* Buffalo Tom
    * Role: Support
    * Order: 2

Events can be different kinds, e.g. "gig", "movie", "play". This is only used for cateegorising Events into different lists - it doesn't restrict the kinds of Works that can be associated with it. You could have a "movie" Event that has a movie, play and dance piece associated with it.

Each Event can have zero or more Works associated with it: movies, plays, classical works or dance pieces. Each Work can have zero or more Creators, each with optional roles, associated directly with it. e.g. "Wolfgang Amadeus Mozart (Composer)",
"William Shakespeare (Playwright)" or "Steven Spielberg (Director)":

Events can be given an optional title (e.g. "Glastonbury Festival"). If a title
isn't specified one is created automatically when needed, based on any Works
associated with it, or else any Creators associated with it.


*************
Template tags
*************

Each app, `core`, `events` and `reading`, has some template tags.

Events template tags
====================

To use any of these in a template, first::

    {% load spectator_events %}

Recent Events
-------------

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
---------------

To get a QuerySet of Events that happened on a particular day, use
``day_events``. If ``my_date`` is a python ``date`` object::

    {% day_events date=my_date as events %}

And display the results as in the above example.

Or to display as a Bootstrap card::

    {% day_events_card date=my_date %}

Years of Events
---------------

To get a QuerySet of the years in which Events happened::

    {% events_years as years %}

    {% for year in years %}
        {{ year|date:"Y" }}<br>
    {% endfor %}

Or to display as a Bootstrap card, with each year linking to the
``EventYearArchiveView``::

    {% events_years_card current_year=year %}

Here, ``year`` is a date object indicating a year which shouldn't be linked.

Reading template tags
=====================

To use any of these in a template, first::

    {% load spectator_reading %}

In-progress Publications
------------------------

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
--------------------------------

To get a QuerySet of Publications that were being read on a particular day use
``day_publications``. If ``my_date`` is a python ``date`` object::

    {% day_publications date=my_date as publications %}

And display the results as in the above example.

Or to display as a Bootstrap card::

    {% day_publications_card date=my_date %}

Years of reading
----------------

To get a QuerySet of the years in which Publications were being read::

    {% reading_years as years %}

    {% for year in years %}
        {{ year|date:"Y" }}<br>
    {% endfor %}

Or to display as a Bootstrap card, with each year linking to the
``ReadingYearArchiveView``::

    {% reading_years_card current_year=year %}

Here, ``year`` is a date object indicating a year which shouldn't be linked.


*****************
Local development
*****************

``devproject/`` is a basic Django project to use the app locally. Use it like::

$ pip install -r devproject/requirements.txt
$ python setup.py develop
$ ./devproject/manage.py migrate
$ ./devproject/manage.py runserver

Run tests with tox. Install it with::

$ pip install tox

Run all tests in all environments like::

$ tox

To run tests in only one environment, specify it. In this case, Python 3.6 and Django 2.0::

$ tox -e py36-django20

To run a specific test, add its path after ``--``, eg::

$ tox -e py36-django20 -- tests.core.test_models.CreatorTestCase.test_ordering

Running the tests in all environments will generate coverage output. There will also be an ``htmlcov/`` directory containing an HTML report. You can also generate these reports without running all the other tests::

$ tox -e coverage

Making a new release
====================

So I don't forget...

1. Put new changes on ``master``.
2. Update the ``__version__`` in ``spectator.__init__.py``.
3. Update ``CHANGES.rst``.
4. Do ``python setup.py tag``.
5. Do ``python setup.py publish``.


Adding a new event type
=======================

If it's simple (like, Gigs, Comedy, etc.) and doesn't require any specific kind of Works, then:

* In ``spectator.events.models.Event`` add it in ``KIND_CHOICES`` and ``KIND_SLUGS``.
* Possibly add a special case for it in ``Event.get_kind_name_plural()``.
* Add a simple factory for it in ``spectator.events.factories``.
* In ``tests.events.test_models.EventTestCase``:
    * Add it to:
        * ``test_get_kind()``
        * ``test_valid_kind_slugs()``
        * ``test_kind_slug()``
        * ``test_kind_name()``
        * ``test_kind_name_plural()``
        * ``test_get_kinds_data()``
    * Add a ``test_absolute_url_*()`` test for this kind.

To add a new kind of Work:

* In ``spectator.events.models.Work`` add it in ``KIND_CHOICES`` and ``KIND_SLUGS``.
* On the ``Event`` model add a new method similar to ``get_classical_works()`` for this new kind of ``Work``.
* On the ``spectator.core.models.Creator`` model add a new method similar to ``get_classical_works()`` for this new kind of ``Work``.
* In ``spectator/events/templates/spectator_events/event_detail.html`` add an include to list the
  works.
* In ``spectator/core/templates/spectator_core/creator_detail.html`` add an include to
  list the works.
* Add tests.

*******
Contact
*******

* Phil Gyford
* phil@gyford.com
* @philgyford on Twitter
