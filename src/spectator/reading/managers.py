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
            .values("kind", "created_date", "first_reading_date")
        )
        book = self.model.Kind.BOOK
        periodical = self.model.Kind.PERIODICAL

        events = defaultdict(lambda: {book: 0, periodical: 0})

        for pub in publications:
            kind = pub["kind"]
            events[pub["created_date"]][kind] += 1

            if pub["first_reading_date"] is not None:
                events[pub["first_reading_date"]][kind] -= 1

        counts = {}
        book_count = 0
        periodical_count = 0
        event_dates = sorted(events.items())
        event_index = 0

        for target_date in sorted(dates):
            while (
                event_index < len(event_dates)
                and event_dates[event_index][0] <= target_date
            ):
                _, changes = event_dates[event_index]
                book_count += changes[book]
                periodical_count += changes[periodical]
                event_index += 1

            counts[target_date] = {
                "book": book_count,
                "periodical": periodical_count,
                "total": book_count + periodical_count,
            }

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
