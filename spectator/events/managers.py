from django.db import models
from django.db.models import Count


class VenueManager(models.Manager):

    def by_visits(self, event_kind=None):
        """
        Gets Venues in order of how many Events have been held there.
        Adds a `num_visits` field to each one.

        event_kind filters by kind of Event, e.g. 'theatre', 'cinema', etc.
        """
        qs = self.get_queryset()

        if event_kind is not None:
            qs = qs.filter(event__kind=event_kind)

        qs = qs.annotate(num_visits=Count('event')) \
                .order_by('-num_visits', 'name_sort')

        return qs


class WorkManager(models.Manager):

    def by_views(self, kind=None):
        """
        Gets Works in order of how many times they've been attached to
        Events.

        kind is the kind of Work, e.g. 'play', 'movie', etc.
        """
        qs = self.get_queryset()

        if kind is not None:
            qs = qs.filter(kind=kind)

        qs = qs.annotate(num_views=Count('event')) \
                .order_by('-num_views', 'title_sort')

        return qs
