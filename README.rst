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

For Django 1.11 to Django 2.2, running on Python 3.5 to 3.7.

It has URLs, views and templates to create a site displaying all the data, and
Django admin screens to add and edit them. The templates use `Bootstrap v4.3 <https://getbootstrap.com>`_.

There are also template tags for displaying data in your own templates (see
below).

This is used on my personal website (with custom templates): `reading <https://www.gyford.com/phil/reading/>`_ and `events <https://www.gyford.com/phil/events/>`_.


************
Installation
************

Install `Pillow <https://python-pillow.org>`_ or `PIL <http://www.pythonware.com/products/pil/>`_ (used by `ImageKit <https://django-imagekit.readthedocs.io/en/latest/>`_ to create thumbnail images).

Install with pip::

    pip install django-spectator

Add these apps to your project's ``INSTALLED_APPS`` in ``settings.py``::

    INSTALLED_APPS = [
        ...
        'imagekit',
        'spectator.core',
        'spectator.events',
        'spectator.reading',
    ]

While ``spectator.core`` is required, you can omit either ``spectator.events``
or ``spectator.reading`` if you only want to use one of them.

``imagekit`` is required to handle uploaded publication cover and event
ticket images.

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

There are a few optional settings that can be used in your project's
``settings.py`` file. This is the full list, with their defaults. Descriptions
of each are below::

    SPECTATOR_GOOGLE_MAPS_API_KEY = ""

    SPECTATOR_SLUG_ALPHABET = "abcdefghijkmnopqrstuvwxyz23456789"

    SPECTATOR_SLUG_SALT = "Django Spectator"

    SPECTATOR_DATE_FORMAT = "%-d %b %Y"

    SPECTATOR_THUMBNAIL_DETAIL_SIZE = (320, 320)

    SPECTATOR_THUMBNAIL_LIST_SIZE = (80, 160)

    SPECTATOR_EVENTS_DIR_BASE = "events"

    SPECTATOR_READING_DIR_BASE = "reading"

If you get a `Google Maps JavaScript API key <https://developers.google.com/maps/documentation/javascript/get-api-key>`_ and
add it to the settings, it will enable using a map in the Django Admin to set
the location of Venues, and the displaying of Venues' maps in the public
templates::

    SPECTATOR_GOOGLE_MAPS_API_KEY = "YOUR-API-KEY"

URLs for all objects include automatically-generated slugs, which are based on
[Hashids](http://hashids.org) of the object's ID. You can change which
characters are used in these slugs with this setting. e.g.::

    SPECTATOR_SLUG_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"

You can also change the salt value used to encode the slugs. While the slugs
don't provide complete security (i.e. it's not impossible to determine the ID on
which a slug is based), using your own salt value can't hurt. e.g.::

    SPECTATOR_SLUG_SALT = "My special salt value is here"

You can change the format used for the dates of Events and for the titles of
some sidebar cards in templates, using `strftime <http://strftime.org>`_ formatting::

    SPECTATOR_DATE_FORMAT = "%Y-%m-%d"

There are two sizes of thumbnail images used throughout the site and admin
pages: those used on "detail" pages (e.g. showing information about a single
publication) and those used on "list" pages (e.g. listing many Publications).
Each thumbnail's maximum size is defined as a tuple of width and height. The
original image will be resized to fit within these limits, without being
cropped. To make them both bigger than the default you might use::

    SPECTATOR_THUMBNAIL_DETAIL_SIZE = (400, 400)

    SPECTATOR_THUMBNAIL_LIST_SIZE = (150, 200)

When images are uploaded for Publications and Events (see below), they are
stored within named directories within your Django project's `MEDIA_ROOT`. e.g.
a Publication with a ``slug`` of ``pzov6`` would have its cover uploaded to
a path like ``/media/reading/publications/pzov6/my_cover.jpg``. The ``reading``
part is defined by the ``SPECTATOR_READING_DIR_BASE`` setting. You could change
the defaults like this::

    SPECTATOR_EVENTS_DIR_BASE = "my-events"

    SPECTATOR_READING_DIR_BASE = "my-reading"


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
performers at a gig, the comedians at a comedy event. These can be in a specific
order, and each with an optional role. e.g:

* The Wedding Present
    * Role: Headliner
    * Order: 1
* Buffalo Tom
    * Role: Support
    * Order: 2

Events can be different kinds, e.g. "gig", "cinema", "theatre". This is only used for categorising Events into different lists - it doesn't restrict the kinds of Works that can be associated with it. You could have a "cinema" Event that has a movie, play and dance piece associated with it.

Each Event can have zero or more Works associated with it: movies, plays, classical works or dance pieces. Each Work can have zero or more Creators, each with optional roles, associated directly with it. e.g. "Wolfgang Amadeus Mozart (Composer)",
"William Shakespeare (Playwright)" or "Steven Spielberg (Director)":

Events can be given an optional title (e.g. "Glastonbury Festival"). If a title
isn't specified one is created automatically when needed, based on any Works
associated with it, or else any Creators associated with it.


*************
Template tags
*************

Each app, `core`, `events` and `reading`, has some template tags.

Core template tags
==================

To use any of these in a template, first::

    {% load spectator_core %}

Most Read Creators
------------------

To get a QuerySet of Creators with the most Readings associated with them::

    {% most_read_creators num=10 %}

Each Creator will have a ``num_readings`` attribute. It will only include
Creators whose role on a publication was "Author" or was left blank. i.e.
Creators who were "Illustrator" or "Translator" would not be counted.

To display this as a chart in a Bootstrap card::

    {% most_read_creators_card num=10 %}

This will exclude any Creators with only 1 Reading.

Most Visited Venues
-------------------

To get a QuerySet of Venues with the most Events associated with them::

    {% most_visited_venues num=10 %}

Each Venue will have a ``num_visits`` attribute.

To display this as a chart in a Bootstrap card::

    {% most_visited_venues_card num=10 %}

This will exclude any Venues with only 1 Event.


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

Annual reading counts
---------------------

For more detail than the ``reading_years`` tag, use this to get the number of
Books, and Periodicals (and the total) finished per year::

    {% annual_reading_counts as years %}

    {% for year_data in years %}
        {{ year_data.year }}:
        {{ year_data.book }} book(s),
        {{ year_data.periodical }} periodical(s),
        {{ year_data.total }} total.<br>
    {% endfor %}

Or to display as a Bootstrap card, with each year linking to ``ReadingYearArchiveView``::

    {% annual_reading_counts_card current_year=year kind='all' %}

Here, ``year`` is a date object indicating a year which shouldn't be linked.

And ``kind`` can be one of "all" (default), "book" or "periodical". If it's "all",
then the result is rendered as a table, with a column each for year, book count,
periodical count and total count. Otherwise it's a list of years with the
book/periodical counts in parentheses.


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

Annual Event Counts
-------------------

To include counts of Events per year::

    {% annual_event_counts as years %}

    {% for year_data in years %}
        {{ year_data.year|date:"Y" }}: {{ year_data.total }} event(s)<br>
    {% endfor %}

Restrict to one kind of Event::

    {% annual_event_counts kind='cinema' as years %}

Or to display as a Bootstrap card, with each year linking to ``EventYearArchiveView``::

    {% annual_event_counts_card current_year=year kind='all' %}

Here, ``year`` is a date object indicating a year which shouldn't be linked.

Most Seen Creators
------------------

To get a QuerySet of Creators involved with the most Events::

    {% most_seen_creators num=10 event_kind='gig' %}

Each Creator will have a ``num_events`` attribute.

``event_kind`` can be omitted, or be ``None`` to include all kinds of Event.

To display this as a chart in a Bootstrap card::

    {% most_seen_creators_card num=10 event_kind='gig' %}

This will exclude any Creators with only 1 Event.

Creators With Most Works
------------------------

To get a QuerySet of Creators that have the most Works (e.g, movies, plays, etc)::

    {% most_seen_creators_by_works num=10 work_kind='movie', role_name='Director' %}

Each Creator will have a ``num_works`` attribute.

``work_kind`` can be omitted and all kinds of Work will be counted.

``role_name`` can be omitted and all roles will be counted.

The above example would, for each Creator, only count movie Works on which their
role was 'Director'.

To display this as a chart in a Bootstrap card::

    {% most_seen_creators_by_works_card num=10 work_kind='movie', role_name='Director' %}

This will exclude any Creators with only 1 Work.


Most Seen Works
---------------

To get a QuerySet of Works involved with the most Events::

    {% most_seen_works num=10 kind='movie' %}

Each Work will have a ``num_views`` attribute.

``kind`` can be omitted, or be ``None`` to include all kinds of Work.

To display this as a chart in a Bootstrap card::

    {% most_seen_works_card num=10 kind='movie' %}

This will exclude any Works with only 1 Event.


*****************
Local development
*****************

``devproject/`` is a basic Django project to use the app locally. Use it like this, installing requirements with pipenv::

$ cd devproject
$ pipenv install
$ pipenv run ./manage.py migrate
$ pipenv run ./manage.py runserver

Run tests with tox, from the top-level directory (containing setup.py). Install it with::

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


Adding a new Event kind
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


Adding a new Work kind
======================

* In ``spectator.events.models.Work`` add it in ``KIND_CHOICES`` and ``KIND_SLUGS``.
* On the ``Event`` model add a new method similar to ``get_classical_works()`` for this new kind of ``Work``.
* On the ``spectator.core.models.Creator`` model add a new method similar to ``get_classical_works()`` for this new kind of ``Work``.
* Add a simple factory for it in ``spectator.events.factories``.
* In ``spectator/events/templates/spectator_events/event_detail.html`` add an include to list the
  works.
* In ``spectator/core/templates/spectator_core/creator_detail.html`` add an include to
  list the works.
* In ``tests/`` add equivalents of:
    * ``core.test_models.CreatorTestCase.test.get_classical_works()``
    * ``events.test_models.EventTestCase.test_get_classical_works()``
    * ``events.test_models.WorkTestCase.test_absolute_url_classicalwork()``
    * ``events.test_models.WorkTestCase.test_get_list_url_classicalwork()``


*******
Contact
*******

* Phil Gyford
* phil@gyford.com
* @philgyford on Twitter
