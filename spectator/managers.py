from django.db import models
from django.db.models import F


class InProgressPublicationsManager(models.Manager):
    """
    Returns Publications that are currently being read.
    They might have previously been finished.
    """
    def get_queryset(self):
        from .models import Publication
        return super().get_queryset().filter(
                                        reading__start_date__isnull=False,
                                        reading__end_date__isnull=True)


class UnreadPublicationsManager(models.Manager):
    """
    Returns Publications that haven't been started (have no Readings).
    """
    def get_queryset(self):
        from .models import Publication
        return super().get_queryset().filter(reading__isnull=True)


class EndDateAscendingManager(models.Manager):
    """
    Returns Readings in descending end_date order, with Readings that have
    no end_date first.
    Via http://stackoverflow.com/a/15125261/250962
    """
    def get_queryset(self):
        from .models import Reading
        qs = super().get_queryset()
        qs = qs.extra(select={'end_date_null': 'end_date is null'})
        return qs.extra(order_by=['end_date_null', 'end_date'])

class EndDateDescendingManager(models.Manager):
    """
    Returns Readings in ascending end_date order, with Readings that have
    no end_date last.
    Via http://stackoverflow.com/a/15125261/250962
    """
    def get_queryset(self):
        from .models import Reading
        qs = super().get_queryset()
        qs = qs.extra(select={'end_date_null': 'end_date is null'})
        return qs.extra(order_by=['-end_date_null', '-end_date'])


