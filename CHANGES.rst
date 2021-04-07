Changelog (Django Spectator)
============================


Unreleased
----------

- None


11.6.0 - 2021-04-07
-------------------

- Include support for Django 3.2.

- Fix: Stop the "Most Read Authors" card counting unfinished Readings.


11.5.0 - 2021-03-23
-------------------

- Add a management command (``generate_letterboxd_export``) that generates a CSV
  file of movies seen, suitable for importing into a Letterboxd.com account.

- Update development project dependencies.

- Update included Bootstrap CSS from 4.5.3 to 4.6.0.


11.4.0 - 2020-12-21
-------------------

- Update python dependencies, including allowing django-debug-toolbar v3,
  frezegun up to v2, pillow up to v9.

- Update Mapbox GL for Venue maps from v1.6.1 to v2.0.0.
  See the `Mapbox GL Changelog <https://github.com/mapbox/mapbox-gl-js/blob/main/CHANGELOG.md>`_.

- Update included Bootstrap CSS from 4.5.2 to 4.5.3.

- Change text "Publication Series" to "Series" in the
  `reading/includes/card_nav.html` template.

- Make counts in `.nav-tabs` consistently `<small>` in templates.

- Add missing migrations


11.3.0 - 2020-08-22
-------------------

- Allow usage of Factory Boy v3


11.2.0 - 2020-08-10
-------------------

- Move Bootstrap CSS files from ``/static/css/`` to ``/static/spectator-core/css/``.


11.1.0 - 2020-08-10
-------------------

- Drop official support for python 3.5.

- Allow usage of Django 3.1, Pillow 7.2, hashids 1.3.

- Upgrade included Bootstrap CSS from v4.4 to v4.5.

- Add flake8 to tests.


11.0.1
------

- Fix display of thumbnails in templates.


11.0.0
------

- Drop support for Django 1.11 and 2.1

- Switch from using django-imagekit specs in ``spectator/core/imagegenerators.py``
  to adding ``ImageSpecField``s directly on the ``Publication`` and ``Event`` models.
  - The ``spectator_core/includes/thumbnail_*.html`` templates have been updated.
  - The old image specs in ``imagegenerators.py`` are deprecated and should no longer be used. They will be removed in a future release.
  - This change means working with models' thumbnails is a little easier. e.g. if django-imagekit's "Optimistic" cache file strategy is used, all of a model's thumbnail sizes will have cached files generated when its thumbnail is added or changed.
- Allow use of pillow up to v7.2 (from v6.3)

- Update Boostrap CSS files from v4.3.1 to v4.4.1

- Make devproject's python dependencies a little laxer


10.0.1
------

- Fix issue where the Mapbox map didn't load when creating a new venue in
  admin.

- Fix issue where the Mapbox venue map marker moved when zooming out.

- Reduce geocoding API calls from Venue add/change admin page.

- Update devproject's Django version from 3.0.0 to 3.0.2


10.0.0
------

- Breaking change: The ``SPECTATOR_GOOGLE_MAPS_API_KEY`` is no longer
  supported. See the README for the new ``SPECTATOR_MAPS`` setting that
  replaces it.

- Add option to use Mapbox for Venue maps and geocoding, instead of Google. SEe
  the ``SPECTATOR_MAPS`` setting.

- Checked that it works with Python 3.8 and Django 3.0.


9.1.0
-----

- If the end reading dates for all publications on a year archive page only
  have year granularity, don't show the months (which was always "January").

- Add ``loading="lazy"`` to thumbnail images in lists (only works on Chrome).

- Fix sort order of names that end with parentheses like "Sam Taylor (1)".


9.0.1
-----

- Increase thumbnail JPEG quality from 60 to 80.


9.0.0
-----

- Add two ImageFields for uploading images: ``Publication.cover`` and
  ``Event.ticket``.

- Now installs `ImageKit <https://django-imagekit.readthedocs.io/en/latest/>`_
  (which needs `Pillow <https://python-pillow.org>`_ or `PIL <http://www.pythonware.com/products/pil/>`_ to be installed first)

- Publication cover images are displayed in a publication's detail template,
  and in lists, but not in the sidebar cards. Also in the Admin.

- Event ticket images are displayed in an event's detail template and in the
  Admin.

- There are new settings (with defaults) related to these images:
  ``SPECTATOR_THUMBNAIL_DETAIL_SIZE``, ``SPECTATOR_THUMBNAIL_LIST_SIZE``,
  ``SPECTATOR_EVENTS_DIR_BASE`` and ``SPECTATOR_READING_DIR_BASE``. See the
  README for more details.


8.8.0
-----

- Update included Bootstrap CSS from 4.1 to 4.3.


8.7.2
-----

- Ensure works with Django 2.2.

- Stop testing in Python 3.4 and/or Django 2.0.


8.7.1
-----

- Stopped HTML tag appearing in the ``title`` tag of Event Detail template.


8.7.0
-----

- Ensure works with Django 2.1.

- Change to use pipenv for managing devproject dependencies.

- Add ``spectator.reading.utils.annual_reading_counts()`` method.

- Add 'Books' and 'Periodicals' tabs to Reading Year Archive pages.


8.6.3
-----

- Upgrade Django used in devproject to 2.0.5.

- Upgrade Bootstrap from v4.1.0 to v4.1.1.


8.6.2
-----

- Add missing migration.

8.6.1
-----

- Undid/simplified some of the previous date-related settings; needs more thought.

8.6.0
-----

Core
~~~~

- Remove leading ``www.`` from visible display of domains when URLizing them.

- Better handle default settings.

Reading
~~~~~~~

- Add optional settings to customise the format of dates when displaying
  Readings.

- Stop possibility of a Publication appearing more than once when listing
  Publications being read on a specific day.

- Order in-progress Publications by when they were started to be read.

Events
~~~~~~

- Turn Exhibitions into a new kind of Work:

    * Renamed ``"exhibition"`` Events to be ``"museum"`` (Museum/Gallery) Events.

    * Added ``"exhibition"`` as a new Work kind.

    * Added a migration to add an Exhibition Work to every Museum/Gallery Event,
      and move any Creator(s) over to that Work.

- Add optional settings to customise the format of Event dates in templates.

- Display the number of Events on a Venue detail page.


8.5.2
-----

- Add ``Creator.get_events()`` method for more accurate counting.

- Fix bug with counting Events or Works multiple times when counting a Creator's
  Events/Works and they had more than one role on an Event/Work.

- Add counts of Venues and Movies/Plays/etc on their list pages.


8.5.1
-----

- Tweaked ``spectator_core/includes/chart.html`` template to allow multiple
  objects per chart position.


8.5.0
-----

- Added template tags for getting the Creators with the most Works.

8.4.0
-----

- Added several manager methods for getting Creators, Venues and Works ordered
  by things such as most-read, most-visited, most-seen, etc.

- Added template tags for displaying charts of the above (and used them in
  templates).

- Added ``annual_reading_counts_card`` template tag  for displaying a table of
  how many books and/or periodicals were finished each year.

- A few template fixes/tweaks.

8.3.0
-----

- Rationalise the usage of 'nav' cards in sidebars.

- Fix the titles and breadcrumbs of the Work List templates.

8.2.0
-----

- Added ``title_html`` property to ``Event`` model, which wraps the names of any
  Works in the title in ``<cite></cite>`` tags.

8.1.0
-----

- Change theatre and cinema Events' 'kind' fields from 'movie' and 'play' to
  'cinema' and 'theatre'.

- Ensure 'sort' fields on models are trimmed to the correct length if greater
  than their ``max_length``.

- Some template tweaks, including to Event list/detail templates' title
  tags.

8.0.0
-----

- Combined ClassicalWorks, DancePieces, Movies and Plays into a single Work
  model, distinguished with a ``kind`` field. Makes things much simpler.

7.3.1
-----

- Make ``cinema_treasures_id`` a ``PositiveIntegerField`` instead of a
  ``PositiveSmallIntegerField``.

7.3.0
-----

- Add a ``venue_name`` field to Events. This remains the same even if the
  attaached Venue object changes its name in the future. The new ``venue_name``
  is used in templates related to the Event.

7.2.0
-----

- Add an optional ``cinema_treasures_id`` field, and ``cinema_treasures_url``
  property, to the Venue model.

7.1.3
-----

- Fix the Event Year Archive view for Events with no Venue.

7.1.2
-----

- Fix templates for Events with no Venue.

7.1.1
-----

- Fix bug with adding an Event with no Venue.

7.1.0
-----

- Upgrade Bootstrap, for the included templates, to v4.0.0.

- Allow Events to not specify a Venue.

- Add a ``note`` field to the Venue model.

7.0.2
-----

- Fix the setting of Events' ``title_sort`` field when saving them in Admin.

7.0.1
-----

- Fix order of works (Movies, Plays, etc) on EventDetail pages.

7.0.0
-----

- An Event can have more than one Movie or Play.

- An Event can have multiple Classical Works, Dance Pieces, Movies or Plays,
  no matter what 'kind' it is.

- Each type of work (Movie, Classical Work, etc.) can be put in a specific order
  within an Event.

- Removed old imports for Django 1.10 and below.

- Various other internal tweaks.

6.0.0
-----

- Rationalise (change) URLs around Events, Movies and Plays. It used to be that
  Movies' and Plays' Detail page served as the place where their Events were
  listed. That's still the case, but now we also have individual Event Detail
  pages for Movie- and Play-related Events.

- Change URLs of Dance Pieces and Classical Works. From
  ``/events/classical/works/`` to ``/events/classical-works/`` and from
  ``/events/dance/pieces/`` to ``/events/dance-pieces/``.

- Fix some templates when there's missing Venue address or country.

- In Venue admin list, in the countries filter, only show countries in use.

- A few other bits of template tidying.

5.2.0
-----

- Add a Note field to Events.

- Add JavaScript to the Admin Event Change form to show/hide fields that aren't required for the chosen Event kind.

5.1.3
-----

- Remove some leading and trailing spaces within links in some templates (also in 5.1.1 and 5.1.2)

5.1.1
-----

- Fix display of a movie's year if `USE_THOUSAND_SEPARATOR` is True

5.1.0
-----

- Fix broken migration for Creators.

5.0.0
-----

- All URL slugs have changed again. Now based on Hashids of objects' IDs.

4.1.0
-----

- Update Bootstrap to v4 beta 3.

4.0.1
-----

- Fix README formatting.

4.0.0
-----

- Works in Django 2.0.
- No longer works in Django 1.8.

3.3.0
-----

- Use slugs in all URLs, rather than PKs. Which means all the URLs for objects have changed.

- Added ``Sitemap`` classes for all the main objects, and used them in the
  devproject urlconf.

3.2.3
-----

- Fix bug in ``day_publications`` template tag.

3.2.2
-----

- Upgrade Bootstrap to v4 beta.

3.1.0
-----

- Change URL namespaces. The ``spectator.core.urls`` conf should now be included under the ``spectator`` namespace.

3.0.0
-----

- The apps all have new labels (e.g., ``spectator_core`` instead of ``core`` to make them less likely to clash with other apps. But this breaks everything, so all-new migrations again.
