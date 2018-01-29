Changelog (Django Spectator)
============================

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
