from django.db import models
from django.db.models import Count


class CreatorManager(models.Manager):

    def by_publications(self):
        """
        The Creators who have been most-read, ordered by number of read
        publications (ignoring if any of those publicatinos have been read
        multiple times.)
        """
        qs = self.get_queryset()

        qs = qs.exclude(publications__reading__isnull=True) \
                .annotate(num_publications=Count('publications')) \
                .order_by('-num_publications', 'name_sort')

        return qs

    def by_readings(self):
        """
        The Creators who have been most-read, ordered by number of readings.
        """
        qs = self.get_queryset()

        qs = qs.exclude(publications__reading__isnull=True) \
                .annotate(num_readings=Count('publications__reading')) \
                .order_by('-num_readings', 'name_sort')

        return qs
