from collections import defaultdict
from datetime import date

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
        """
        Get the number of Publications that were unread on each of a list of dates.

        e.g.
            from datetime import date

            dates = (
                date(2026, 6, 1),
                date(2026, 7, 1),
                date(2026, 8, 1),
            )

            counts = Publication.unread_objects.get_counts_for_dates(dates)

        Returns a dict like:

            {
                date(2026, 8, 3): {
                    "book": 34,
                    "periodical": 7,
                    "total": 41
                },
                ...
            }

        It will ignore any Publications that were added to the database after
        their first Reading dates (which can happen if adding historical
        data to the database).

        Args:
        - dates - a list of date objects to get counts for.
        """
        if isinstance(dates, list) is False:
            msg = "The dates argument should be a list"
            raise TypeError(msg)

        if len(dates) > 0 and isinstance(dates[0], date) is False:
            msg = f"""The dates argument should be a list of date
                objects; the first item is of type {type(dates[0])}"""
            raise TypeError(msg)

        # First, for every Publication, we get the date it was created
        # and the first date it was read (or started to be read), if any.
        publications = (
            super()
            .get_queryset()
            .annotate(
                created_date=TruncDate("time_created"),
                # Get earliest time it was read, allowing for empty start/end:
                first_reading_date=Min(
                    Case(
                        When(
                            reading__start_date__isnull=False,
                            then="reading__start_date",
                        ),
                        When(
                            reading__end_date__isnull=False,
                            then="reading__end_date",
                        ),
                    )
                ),
            )
            .values("kind", "created_date", "first_reading_date")
        )

        book = self.model.Kind.BOOK
        periodical = self.model.Kind.PERIODICAL

        # Now we go through those Publications and create a count of when
        # each Publication was unread. Usually it counts (+1) from the date
        # it was created, until (-1) it was first read.
        events = defaultdict(lambda: {book: 0, periodical: 0})

        for publication in publications:
            kind = publication["kind"]
            created_date = publication["created_date"]
            reading_date = publication["first_reading_date"]

            if reading_date is None:
                # This hasn't been read at all, so +1 from the date it was created
                events[created_date][kind] += 1
            elif reading_date > created_date:
                # It has been read, so +1 for when it was created,
                # and -1 at the point it was read.
                events[created_date][kind] += 1
                events[reading_date][kind] -= 1
            # Else, if it was read before it was added (eg this was
            # data added from some offline source), then we don't count it at
            # all because we don't know when it would have been 'created'
            # before it was read.

        counts = {}
        book_count = 0
        periodical_count = 0
        event_dates = sorted(events.items())
        event_index = 0

        # Finally, for each of our chosen dates, we look at the events.
        # We add up all the points up until the chosen date, then record
        # that total for books, periodicals, and total, for each date.
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
