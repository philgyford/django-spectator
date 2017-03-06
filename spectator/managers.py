from django.db import models


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

