from django.db import models
from django.db.models import Count


class VenueManager(models.Manager):

    def by_visits(self, event_kind=None):
        qs = self.get_queryset()

        if event_kind is not None:
            qs = qs.filter(event__kind=event_kind)

        qs = qs.annotate(num_visits=Count('event')) \
                .order_by('-num_visits', 'name_sort')

        return qs
