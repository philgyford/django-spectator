Changelog (Django Spectator)
============================


5.1.3
-----

-- Remove some leading and trailing spaces within links in some templates (also in 5.1.1 and 5.1.2)

5.1.1
-----

-- Fix display of a movie's year if `USE_THOUSAND_SEPARATOR` is True

5.1.0
-----

-- Fix broken migration for Creators.

5.0.0
-----

-- All URL slugs have changed again. Now based on Hashids of objects' IDs.

4.1.0
-----

-- Update Bootstrap to v4 beta 3.

4.0.1
-----

-- Fix README formatting.

4.0.0
-----

-- Works in Django 2.0.
-- No longer works in Django 1.8.

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
