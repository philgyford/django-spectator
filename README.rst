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

So far only used with Python 3.6 and Django 1.10 or 1.11. Should work with
Python 3.5+ and Django 1.8+.

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

Add to your project's ``urls.py`` with the ``'spectator'`` namespace::

    urlpatterns = [
        # ...

        url(r'^spectator/', include('spectator.core.urls', namespace='spectator')),
    ] 

You can change the initial path (``r'^spectator/'``) to whatever suits you. e.g.
use ``r'^'`` to have Spectator's home page be the front page of your site.

Optionally get a `Google Maps JavaScript API key <https://developers.google.com/maps/documentation/javascript/get-api-key>`_ and add it to your ``settings.py`` like this::

    SPECTATOR_GOOGLE_MAPS_API_KEY = 'YOUR-API-KEY'

This will enable using a map in the Django Admin to set the location of Venues,
and the displaying of Venues' maps in the public templates.

Then, go to Django Admin to add your data.


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
A Venue has a name and, optionally, location details. Events can be different
kinds, e.g. "gig", "movie", "play".

While an Event is a thing at a place on a day, with some optional Creators,
some kinds of Events are slightly more complicated.

Gigs, Comedy, Exhibitions and Other 
-----------------------------------

Events of kind "gig", "comedy", "exhibition" and "misc" are the simplest. A
date when you went to a Venue to see one or more Creators. The Event can
optionally have a title. "Other" is for events that don't fit into one of the
other kinds.

Plays
-----

An Event of kind "play" can have one Play object (e.g. "King Lear") connected to
it. A Play is created by (optionally) one or more Creators (e.g. "William 
Shakespeare (Playwright)"). A Play can therefore have several Events (occasions
when you saw that one play), with its own Creators (e.g. "Anthony Sher 
(Actor)").

Movies
------

An Event of kind "movie" can have one Movie object connected to it. A Movie is
created by (optionally) one or more Creators. It can optionally have a year and
an IMDb ID. A Movie can therefore have several Events (occasions when you saw
that one film). Although you could add Creators to the Event itself, that
probably doesn't make sense usually, unless, there was a post-screening
interview or something.

Classical concert
-----------------

An Event of kind "concert" is when one *or more* Classical Works were 
seen/heard. A Classical Work can have zero or more Creators (e.g. "Wolfgang
Amadeus Mozart (Composer)"). The Event itself can also have zero or more
Creators (e.g. "Ian Page (Conductor)").

Dance
-----

An Event of kind "dance" is when one *or more* Dance Pieces were seen. A Dance
Piece can have zero or more Creators (e.g. "Pina Bausch (Choreographer)"). The
Event itself can also have zero or more Creators (e.g. "English National
Ballet").


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

To run tests in only one environment, specify it. In this case, Python 3.6 and Django 1.11::

$ tox -e py36-django111

To run a specific test, add its path after ``--``, eg::

$ tox -e py36-django111 -- tests.core.test_models.CreatorTestCase.test_ordering

Running the tests in all environments will generate coverage output. There will also be an ``htmlcov/`` directory containing an HTML report. You can also generate these reports without running all the other tests::

$ tox -e coverage

Adding a new event type
=======================

If it's simple (like, Gigs, Comedy, etc.) and doesn't require extra models,
then:

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

If it involves an extra model (like Movies and Plays do) then also:

* Create the new model in ``spectator.events.models`` with a matching Role
  model (like ``MovieRole``).
* Associate the new model by ``ForeignKey`` to the ``Event`` model.
* Add a special case for it in ``Event.get_absolute_url()``.
* Add a special case for it in ``Event.__str__()``.
* Add its Admin in ``spectator.events.admin``.
* Add any validation needed to ``spectator.events.admin.EventAdminForm``.
* Add new URLs for the model's List and Detail views in
  ``spectator.events.urls`` (and add tests).
* Add the new List and Detail views in ``spectator.events.views``.
* In ``spectator.events.views.EventDetailView.get_queryset()`` add a section to
  adjust the queryset for this model.
* Add templates in ``spectator/events/templates/events/`` for its List and
  Detail views.
* In ``spectator/core/templates/core/creator_detail.html`` add a section to
  list the new models for a Creator.

If it involves several extra models (like Dance and Concert events do) then
it's similar to above but absolute URLs are different; see the code for
examples of those.

* Instead of adding the new modely by ``ForeignKey``, it's
  a ``ManyToManyField``.
* It doesn't have a special case in ``Event.get_absolute_url()``.
* Add URLs and Views for the List and Detail views for the new model
  (e.g. DancePiece).
* Add the ``get_absolute_url()`` method for that new model.
* Add the display of its works (e.g. DancePieces) in ``spectator/events/templates/events/event_detail.html``.


*******
Contact
*******

Phil Gyford
phil@gyford.com
@philgyford on Twitter


