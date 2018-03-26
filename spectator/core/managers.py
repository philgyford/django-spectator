from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.models import Count

from .apps import spectator_apps


class CreatorManager(models.Manager):

    def by_publications(self):
        """
        The Creators who have been most-read, ordered by number of read
        publications (ignoring if any of those publicatinos have been read
        multiple times.)

        Each Creator will have a `num_publications` attribute.
        """
        if not spectator_apps.is_enabled('reading'):
            raise ImproperlyConfigured("To use the CreatorManager.by_publications() method, 'spectator.reading' must by in INSTALLED_APPS.")

        qs = self.get_queryset()

        qs = qs.exclude(publications__reading__isnull=True) \
                    .annotate(num_publications=Count('publications')) \
                    .order_by('-num_publications', 'name_sort')

        return qs

    def by_readings(self, role_names=['', 'Author']):
        """
        The Creators who have been most-read, ordered by number of readings.

        By default it will only include Creators whose role was left empty,
        or is 'Author'.

        Each Creator will have a `num_readings` attribute.
        """
        if not spectator_apps.is_enabled('reading'):
            raise ImproperlyConfigured("To use the CreatorManager.by_readings() method, 'spectator.reading' must by in INSTALLED_APPS.")

        qs = self.get_queryset()

        qs = qs.filter(publication_roles__role_name__in=role_names) \
                .exclude(publications__reading__isnull=True) \
                .annotate(num_readings=Count('publications__reading')) \
                .order_by('-num_readings', 'name_sort')

        return qs

    def by_events(self, kind=None):
        """
        Get the Creators involved in the most Events.

        This only counts Creators directly involved in an Event.
        i.e. if a Creator is the director of a movie Work, and an Event was
        a viewing of that movie, that Event wouldn't count. Unless they were
        also directly involved in the Event (e.g. speaking after the movie).

        kind - If supplied, only Events with that `kind` value will be counted.
        """
        if not spectator_apps.is_enabled('events'):
            raise ImproperlyConfigured("To use the CreatorManager.by_events() method, 'spectator.events' must by in INSTALLED_APPS.")

        qs = self.get_queryset()

        if kind is not None:
            qs = qs.filter(events__kind=kind)

        qs = qs.annotate(num_events=Count('events', distinct=True)) \
                .order_by('-num_events', 'name_sort')

        return qs

    def by_works(self, kind=None, role_name=None):
        """
        Get the Creators involved in the most Works.

        kind - If supplied, only Works with that `kind` value will be counted.
        role_name - If supplied, only Works on which the role is that will be counted.

        e.g. To get all 'movie' Works on which the Creators had the role 'Director':

            Creator.objects.by_works(kind='movie', role_name='Director')
        """
        if not spectator_apps.is_enabled('events'):
            raise ImproperlyConfigured("To use the CreatorManager.by_works() method, 'spectator.events' must by in INSTALLED_APPS.")

        qs = self.get_queryset()

        filter_kwargs = {}

        if kind is not None:
            filter_kwargs['works__kind'] = kind

        if role_name is not None:
            filter_kwargs['work_roles__role_name'] = role_name

        if filter_kwargs:
            qs = qs.filter(**filter_kwargs)

        qs = qs.annotate(num_works=Count('works', distinct=True)) \
                .order_by('-num_works', 'name_sort')

        return qs
