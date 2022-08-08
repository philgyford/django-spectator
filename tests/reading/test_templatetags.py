from unittest.mock import patch

from django.test import TestCase

from spectator.reading.factories import PublicationFactory, ReadingFactory
from spectator.reading.templatetags.spectator_reading import (
    annual_reading_counts,
    day_publications,
    in_progress_publications,
    reading_dates,
    reading_years,
)

from .. import make_date

# from spectator.reading import utils


class AnnualReadingCountsTestCase(TestCase):
    """
    Ensure the template tag calls the util method with correct arguments.
    """

    def test_default(self):
        with patch("spectator.reading.utils.annual_reading_counts") as mocked_counts:
            annual_reading_counts()
            mocked_counts.assert_called_once_with(kind="all")

    def test_all(self):
        with patch("spectator.reading.utils.annual_reading_counts") as mocked_counts:
            annual_reading_counts(kind="all")
            mocked_counts.assert_called_once_with(kind="all")

    def test_book(self):
        with patch("spectator.reading.utils.annual_reading_counts") as mocked_counts:
            annual_reading_counts(kind="book")
            mocked_counts.assert_called_once_with(kind="book")

    def test_periodical(self):
        with patch("spectator.reading.utils.annual_reading_counts") as mocked_counts:
            annual_reading_counts(kind="periodical")
            mocked_counts.assert_called_once_with(kind="periodical")


class InProgressPublicationsTestCase(TestCase):
    def test_queryset(self):
        "It should return in-progress publications."
        in_progress = ReadingFactory(start_date=make_date("2017-02-10"))
        ReadingFactory(
            start_date=make_date("2017-01-15"), end_date=make_date("2017-01-28")
        )
        qs = in_progress_publications()
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0], in_progress.publication)


class DayPublicationsTestCase(TestCase):
    def test_ended_readings(self):
        "It returns publications whose ended readings were around the date"
        pub1 = PublicationFactory()
        pub2 = PublicationFactory()
        # pub1 started before and ended after the date:
        ReadingFactory(
            publication=pub1,
            start_date=make_date("2017-02-10"),
            end_date=make_date("2017-02-20"),
        )
        # pub2 was over before the date:
        ReadingFactory(
            publication=pub2,
            start_date=make_date("2017-01-01"),
            end_date=make_date("2017-01-10"),
        )
        qs = day_publications(make_date("2017-02-15"))
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0], pub1)

    def test_in_progress_readings(self):
        "It returns publications that were still in progress on the date."
        pub1 = PublicationFactory()
        pub2 = PublicationFactory()
        # pub1 started before the date:
        ReadingFactory(
            publication=pub1, start_date=make_date("2017-02-10"), end_date=None
        )
        # pub2 started after the date:
        ReadingFactory(
            publication=pub2, start_date=make_date("2017-03-01"), end_date=None
        )
        qs = day_publications(make_date("2017-02-15"))
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0], pub1)

    def test_two_readings(self):
        """Shouldn't return a pub if it it had a reading before, and a
        reading after, the chosen date.
        """
        pub = PublicationFactory()
        ReadingFactory(
            publication=pub,
            start_date=make_date("2017-01-01"),
            end_date=make_date("2017-01-31"),
        )
        ReadingFactory(
            publication=pub,
            start_date=make_date("2017-03-01"),
            end_date=make_date("2017-03-31"),
        )
        qs = day_publications(make_date("2017-02-15"))
        self.assertEqual(len(qs), 0)

    def test_unique_publications(self):
        "Should only list each publication once."
        pub = PublicationFactory()
        ReadingFactory(
            publication=pub,
            start_date=make_date("2017-01-01"),
            end_date=make_date("2017-01-31"),
        )
        ReadingFactory(
            publication=pub,
            start_date=make_date("2017-01-31"),
            end_date=make_date("2017-02-15"),
        )
        qs = day_publications(make_date("2017-01-31"))
        self.assertEqual(len(qs), 1)


class ReadingYearsTestCase(TestCase):
    def test_queryset(self):
        ReadingFactory(
            start_date=make_date("2015-02-10"), end_date=make_date("2015-02-15")
        )
        ReadingFactory(
            start_date=make_date("2017-02-10"), end_date=make_date("2017-02-15")
        )
        ReadingFactory(
            start_date=make_date("2017-03-10"), end_date=make_date("2017-03-15")
        )
        qs = reading_years()
        self.assertEqual(len(qs), 2)
        self.assertEqual(qs[0], make_date("2015-01-01"))
        self.assertEqual(qs[1], make_date("2017-01-01"))


class ReadingDatesTestCase(TestCase):

    # Both start_date AND end_date.

    # Granularity both 3.

    def test_ymd_to_ymd_diff_years(self):
        "Complete dates, start and finish in different years"
        r = ReadingFactory(
            start_date=make_date("2016-12-30"),
            start_granularity=3,
            end_date=make_date("2017-01-06"),
            end_granularity=3,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2016-12-30">30 December 2016</time> to <time datetime="2017-01-06">6 January 2017</time>',  # noqa: E501
        )

    def test_ymd_to_ymd_same_year(self):
        "Complete dates, start and finish in different months of same year."
        r = ReadingFactory(
            start_date=make_date("2017-01-30"),
            start_granularity=3,
            end_date=make_date("2017-02-06"),
            end_granularity=3,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2017-01-30">30 January</time> to <time datetime="2017-02-06">6 February 2017</time>',  # noqa: E501
        )

    def test_ymd_to_ymd_same_month(self):
        "Complete dates, start and finish in same month."
        r = ReadingFactory(
            start_date=make_date("2017-02-01"),
            start_granularity=3,
            end_date=make_date("2017-02-06"),
            end_granularity=3,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2017-02-01">1</time>–<time datetime="2017-02-06">6 February 2017</time>',  # noqa: E501
        )

    def test_ymd_to_ymd_same_day(self):
        "Complete dates, start and finish on same day."
        r = ReadingFactory(
            start_date=make_date("2017-02-01"),
            start_granularity=3,
            end_date=make_date("2017-02-01"),
            end_granularity=3,
        )
        self.assertEqual(
            reading_dates(r), '<time datetime="2017-02-01">1 February 2017</time>'
        )

    # Less granular start_dates.

    def test_ym_to_ymd(self):
        "Month-based start date, complete end date"
        r = ReadingFactory(
            start_date=make_date("2016-12-30"),
            start_granularity=4,
            end_date=make_date("2017-01-06"),
            end_granularity=3,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2016-12">December 2016</time> to <time datetime="2017-01-06">6 January 2017</time>',  # noqa: E501
        )

    def test_ym_to_ymd_same_year(self):
        "Month-based start date, complete end date, in same year."
        r = ReadingFactory(
            start_date=make_date("2017-01-01"),
            start_granularity=4,
            end_date=make_date("2017-02-01"),
            end_granularity=3,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2017-01">January</time> to <time datetime="2017-02-01">1 February 2017</time>',  # noqa: E501
        )

    def test_y_to_ymd(self):
        "Year-based start date, complete end date"
        r = ReadingFactory(
            start_date=make_date("2016-12-30"),
            start_granularity=6,
            end_date=make_date("2017-01-06"),
            end_granularity=3,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2016">2016</time> to <time datetime="2017-01-06">6 January 2017</time>',  # noqa: E501
        )

    # Less granular end_dates.

    def test_ymd_to_ym(self):
        "Complete start date, month-based end date."
        r = ReadingFactory(
            start_date=make_date("2016-12-30"),
            start_granularity=3,
            end_date=make_date("2017-01-06"),
            end_granularity=4,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2016-12-30">30 December 2016</time> to <time datetime="2017-01">January 2017</time>',  # noqa: E501
        )

    def test_ymd_to_ym_same_year(self):
        "Complete start date, month-based end date, in same year."
        r = ReadingFactory(
            start_date=make_date("2017-01-01"),
            start_granularity=3,
            end_date=make_date("2017-02-01"),
            end_granularity=4,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2017-01-01">1 January</time> to <time datetime="2017-02">February 2017</time>',  # noqa: E501
        )

    def test_ymd_to_y(self):
        "Complete start date to year-based end date"
        r = ReadingFactory(
            start_date=make_date("2016-12-30"),
            start_granularity=3,
            end_date=make_date("2017-01-06"),
            end_granularity=6,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2016-12-30">30 December 2016</time> to <time datetime="2017">2017</time>',  # noqa: E501
        )

    # Less granular start_date and end_date.

    def test_y_to_y_diff_year(self):
        "Only years for start and end, and different years."
        r = ReadingFactory(
            start_date=make_date("2016-01-01"),
            start_granularity=6,
            end_date=make_date("2017-01-01"),
            end_granularity=6,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2016">2016</time> to <time datetime="2017">2017</time>',
        )

    def test_y_to_y_same_year(self):
        "Only years for start and end, and the same year."
        r = ReadingFactory(
            start_date=make_date("2017-01-01"),
            start_granularity=6,
            end_date=make_date("2017-01-01"),
            end_granularity=6,
        )
        self.assertEqual(reading_dates(r), '<time datetime="2017">2017</time>')

    def test_ym_to_ym_diff_years(self):
        "Month and year for start and end, and different years."
        r = ReadingFactory(
            start_date=make_date("2016-12-01"),
            start_granularity=4,
            end_date=make_date("2017-01-01"),
            end_granularity=4,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2016-12">December 2016</time> to <time datetime="2017-01">January 2017</time>',  # noqa: E501
        )

    def test_ym_to_ym_diff_months_same_year(self):
        "Month and year for start and end, and different months, same year."
        r = ReadingFactory(
            start_date=make_date("2017-01-01"),
            start_granularity=4,
            end_date=make_date("2017-02-01"),
            end_granularity=4,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2017-01">January</time> to <time datetime="2017-02">February 2017</time>',  # noqa: E501
        )

    def test_ym_to_ym_same_month(self):
        "Month and year for start and end, and same month."
        r = ReadingFactory(
            start_date=make_date("2017-01-01"),
            start_granularity=4,
            end_date=make_date("2017-01-01"),
            end_granularity=4,
        )
        self.assertEqual(
            reading_dates(r), '<time datetime="2017-01">January 2017</time>'
        )

    def test_ym_to_ym_same_year(self):
        "Month and year for start and end, and same year."
        r = ReadingFactory(
            start_date=make_date("2017-01-01"),
            start_granularity=4,
            end_date=make_date("2017-02-01"),
            end_granularity=4,
        )
        self.assertEqual(
            reading_dates(r),
            '<time datetime="2017-01">January</time> to <time datetime="2017-02">February 2017</time>',  # noqa: E501
        )

    # Only an end_date.

    def test_end_ymd(self):
        "Complete end date, no start"
        r = ReadingFactory(end_date=make_date("2017-02-01"), end_granularity=3)
        self.assertEqual(
            reading_dates(r),
            'Finished on <time datetime="2017-02-01">1 February 2017</time>',
        )

    def test_end_ym(self):
        "Month-based end date, no start"
        r = ReadingFactory(end_date=make_date("2017-02-01"), end_granularity=4)
        self.assertEqual(
            reading_dates(r),
            'Finished in <time datetime="2017-02">February 2017</time>',
        )

    def test_end_y(self):
        "Year-based end date, no start"
        r = ReadingFactory(end_date=make_date("2017-02-01"), end_granularity=6)
        self.assertEqual(
            reading_dates(r), 'Finished in <time datetime="2017">2017</time>'
        )

    # Only a start_date.

    def test_start_ymd(self):
        "Complete start date, no end"
        r = ReadingFactory(start_date=make_date("2017-02-01"), start_granularity=3)
        self.assertEqual(
            reading_dates(r),
            'Started on <time datetime="2017-02-01">1 February 2017</time>',
        )

    def test_start_ym(self):
        "Month-based start date, no end"
        r = ReadingFactory(start_date=make_date("2017-02-01"), start_granularity=4)
        self.assertEqual(
            reading_dates(r), 'Started in <time datetime="2017-02">February 2017</time>'
        )

    def test_start_y(self):
        "Year-based start date, no end"
        r = ReadingFactory(start_date=make_date("2017-02-01"), start_granularity=6)
        self.assertEqual(
            reading_dates(r), 'Started in <time datetime="2017">2017</time>'
        )
