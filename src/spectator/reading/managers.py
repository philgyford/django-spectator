from collections import defaultdict

from django.db import models
from django.db.models import Case, Min, When
from django.db.models.functions import TruncDate


class InProgressPublicationsManager(models.Manager):
    """
    Returns Publications that are currently being read, ordered with the
    most-recently-started last.
    They might have previously been finished.
    """

    def get_queryset(self):
        from .models import Publication  # noqa: F401

        return (
            super()
            .get_queryset()
            .filter(reading__start_date__isnull=False, reading__end_date__isnull=True)
            .annotate(min_start_date=Min("reading__start_date"))
            .order_by("min_start_date")
        )


class UnreadPublicationsManager(models.Manager):
    """
    Returns Publications that haven't been started (have no Readings).
    """

    def get_queryset(self):
        return super().get_queryset().filter(reading__isnull=True)

    def get_counts_for_dates(self, dates):
        publications = (
            super()
            .get_queryset()
            .annotate(
                created_date=TruncDate("time_created"),
                first_reading_date=Min(
                    Case(
                        When(
                            reading__start_date__isnull=True,
                            then="reading__end_date",
                        ),
                        default="reading__start_date",
                    )
                ),
            )
            .values("created_date", "first_reading_date")
        )

        events = defaultdict(int)

        for publication in publications:
            events[publication["created_date"]] += 1

            if publication["first_reading_date"] is not None:
                events[publication["first_reading_date"]] -= 1

        counts = {}

        running_count = 0
        event_dates = sorted(events.items())
        event_index = 0

        for target_date in sorted(dates):
            while (
                event_index < len(event_dates)
                and event_dates[event_index][0] <= target_date
            ):
                _, change = event_dates[event_index]
                running_count += change
                event_index += 1
            counts[target_date] = running_count

        return counts


class EndDateAscendingReadingsManager(models.Manager):
    """
    Returns Readings in descending end_date order, with Readings that have
    no end_date first.
    Via http://stackoverflow.com/a/15125261/250962
    """

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.extra(select={"end_date_null": "end_date is null"})
        return qs.extra(order_by=["end_date_null", "end_date"])


class EndDateDescendingReadingsManager(models.Manager):
    """
    Returns Readings in ascending end_date order, with Readings that have
    no end_date last.
    Via http://stackoverflow.com/a/15125261/250962
    """

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.extra(select={"end_date_null": "end_date is null"})
        return qs.extra(order_by=["-end_date_null", "-end_date"])
