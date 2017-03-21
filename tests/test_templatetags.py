from unittest.mock import Mock

from django.http import QueryDict
from django.test import TestCase

from . import make_date
from spectator.factories import ConcertFactory, MovieEventFactory,\
        ReadingFactory
from spectator.templatetags.spectator_tags import query_string,\
        in_progress_publications, reading_dates, recent_events


class QueryStringTestCase(TestCase):

    def test_adds_arg(self):
        "It adds your key/value to the existing GET string."
        context = {'request': Mock( GET=QueryDict('a=1') ) }
        self.assertIn(
            query_string(context, 'foo', 'bar'),
            ['foo=bar&a=1', 'a=1&foo=bar']
        )

    def test_replaces_arg(self):
        "It replaces an existing GET arg with what you supply."
        context = {'request': Mock( GET=QueryDict('a=1') ) }
        self.assertEqual(
            query_string(context, 'a', 'bar'),
            'a=bar'
        )

    def test_handles_missing_request(self):
        "If there's no request object, it doesn't complain."
        context = {}
        self.assertEqual(
            query_string(context, 'foo', 'bar'),
            'foo=bar'
        )

    def test_urlencodes(self):
        "It URL-encodes the returned string."
        context = {'request': Mock( GET=QueryDict('a=1') ) }
        self.assertIn(
            query_string(context, 'foo', 'bar&bar'),
            ['foo=bar%26bar&a=1', 'a=1&foo=bar%26bar']
        )


class ReadingDatesTestCase(TestCase):

    # Both start_date AND end_date.

    ## Granularity both 3.

    def test_ymd_to_ymd_diff_years(self):
        "Complete dates, start and finish in different years"
        r = ReadingFactory(start_date=make_date('2016-12-30'),
                           start_granularity=3,
                           end_date=make_date('2017-01-06'),
                           end_granularity=3)
        self.assertEqual(reading_dates(r),
            '<time datetime="2016-12-30">30&nbsp;Dec&nbsp;2016</time> to <time datetime="2017-01-06">6&nbsp;Jan&nbsp;2017</time>')

    def test_ymd_to_ymd_same_year(self):
        "Complete dates, start and finish in different months of same year."
        r = ReadingFactory(start_date=make_date('2017-01-30'),
                           start_granularity=3,
                           end_date=make_date('2017-02-06'),
                           end_granularity=3)
        self.assertEqual(reading_dates(r),
         '<time datetime="2017-01-30">30&nbsp;Jan</time> to <time datetime="2017-02-06">6&nbsp;Feb&nbsp;2017</time>')

    def test_ymd_to_ymd_same_month(self):
        "Complete dates, start and finish in same month."
        r = ReadingFactory(start_date=make_date('2017-02-01'),
                           start_granularity=3,
                           end_date=make_date('2017-02-06'),
                           end_granularity=3)
        self.assertEqual(reading_dates(r),
            '<time datetime="2017-02-01">1</time>–<time datetime="2017-02-06">6&nbsp;Feb&nbsp;2017</time>')

    def test_ymd_to_ymd_same_day(self):
        "Complete dates, start and finish on same day."
        r = ReadingFactory(start_date=make_date('2017-02-01'),
                           start_granularity=3,
                           end_date=make_date('2017-02-01'),
                           end_granularity=3)
        self.assertEqual(reading_dates(r),
            '<time datetime="2017-02-01">1&nbsp;Feb&nbsp;2017</time>')

    ## Less granular start_dates.

    def test_ym_to_ymd(self):
        "Month-based start date, complete end date"
        r = ReadingFactory(start_date=make_date('2016-12-30'),
                           start_granularity=4,
                           end_date=make_date('2017-01-06'),
                           end_granularity=3)
        self.assertEqual(reading_dates(r),
             '<time datetime="2016-12">Dec&nbsp;2016</time> to <time datetime="2017-01-06">6&nbsp;Jan&nbsp;2017</time>')

    def test_ym_to_ymd_same_year(self):
        "Month-based start date, complete end date, in same year."
        r = ReadingFactory(start_date=make_date('2017-01-01'),
                           start_granularity=4,
                           end_date=make_date('2017-02-01'),
                           end_granularity=3)
        self.assertEqual(reading_dates(r),
            '<time datetime="2017-01">Jan</time> to <time datetime="2017-02-01">1&nbsp;Feb&nbsp;2017</time>')

    def test_y_to_ymd(self):
        "Year-based start date, complete end date"
        r = ReadingFactory(start_date=make_date('2016-12-30'),
                           start_granularity=6,
                           end_date=make_date('2017-01-06'),
                           end_granularity=3)
        self.assertEqual(reading_dates(r),
            '<time datetime="2016">2016</time> to <time datetime="2017-01-06">6&nbsp;Jan&nbsp;2017</time>')

    ## Less granular end_dates.

    def test_ymd_to_ym(self):
        "Complete start date, month-based end date."
        r = ReadingFactory(start_date=make_date('2016-12-30'),
                           start_granularity=3,
                           end_date=make_date('2017-01-06'),
                           end_granularity=4)
        self.assertEqual(reading_dates(r),
            '<time datetime="2016-12-30">30&nbsp;Dec&nbsp;2016</time> to <time datetime="2017-01">Jan&nbsp;2017</time>')

    def test_ymd_to_ym_same_year(self):
        "Complete start date, month-based end date, in same year."
        r = ReadingFactory(start_date=make_date('2017-01-01'),
                           start_granularity=3,
                           end_date=make_date('2017-02-01'),
                           end_granularity=4)
        self.assertEqual(reading_dates(r),
            '<time datetime="2017-01-01">1&nbsp;Jan</time> to <time datetime="2017-02">Feb&nbsp;2017</time>')

    def test_ymd_to_y(self):
        "Complete start date to year-based end date"
        r = ReadingFactory(start_date=make_date('2016-12-30'),
                           start_granularity=3,
                           end_date=make_date('2017-01-06'),
                           end_granularity=6)
        self.assertEqual(reading_dates(r),
            '<time datetime="2016-12-30">30&nbsp;Dec&nbsp;2016</time> to <time datetime="2017">2017</time>')

    ## Less granular start_date and end_date.

    def test_y_to_y_diff_year(self):
        "Only years for start and end, and different years."
        r = ReadingFactory(start_date=make_date('2016-01-01'),
                           start_granularity=6,
                           end_date=make_date('2017-01-01'),
                           end_granularity=6)
        self.assertEqual(reading_dates(r),
            '<time datetime="2016">2016</time> to <time datetime="2017">2017</time>')

    def test_y_to_y_same_year(self):
        "Only years for start and end, and the same year."
        r = ReadingFactory(start_date=make_date('2017-01-01'),
                           start_granularity=6,
                           end_date=make_date('2017-01-01'),
                           end_granularity=6)
        self.assertEqual(reading_dates(r), '<time datetime="2017">2017</time>')

    def test_ym_to_ym_diff_years(self):
        "Month and year for start and end, and different years."
        r = ReadingFactory(start_date=make_date('2016-12-01'),
                           start_granularity=4,
                           end_date=make_date('2017-01-01'),
                           end_granularity=4)
        self.assertEqual(reading_dates(r),
            '<time datetime="2016-12">Dec&nbsp;2016</time> to <time datetime="2017-01">Jan&nbsp;2017</time>')

    def test_ym_to_ym_diff_months_same_year(self):
        "Month and year for start and end, and different months, same year."
        r = ReadingFactory(start_date=make_date('2017-01-01'),
                           start_granularity=4,
                           end_date=make_date('2017-02-01'),
                           end_granularity=4)
        self.assertEqual(reading_dates(r),
            '<time datetime="2017-01">Jan</time> to <time datetime="2017-02">Feb&nbsp;2017</time>')

    def test_ym_to_ym_same_month(self):
        "Month and year for start and end, and same month."
        r = ReadingFactory(start_date=make_date('2017-01-01'),
                           start_granularity=4,
                           end_date=make_date('2017-01-01'),
                           end_granularity=4)
        self.assertEqual(reading_dates(r),
            '<time datetime="2017-01">Jan&nbsp;2017</time>')

    def test_ym_to_ym_same_year(self):
        "Month and year for start and end, and same year."
        r = ReadingFactory(start_date=make_date('2017-01-01'),
                           start_granularity=4,
                           end_date=make_date('2017-02-01'),
                           end_granularity=4)
        self.assertEqual(reading_dates(r),
            '<time datetime="2017-01">Jan</time> to <time datetime="2017-02">Feb&nbsp;2017</time>')

    # Only an end_date.

    def test_end_ymd(self):
        "Complete end date, no start"
        r = ReadingFactory(end_date=make_date('2017-02-01'),
                           end_granularity=3)
        self.assertEqual(reading_dates(r),
            'Finished on <time datetime="2017-02-01">1&nbsp;Feb&nbsp;2017</time>')

    def test_end_ym(self):
        "Month-based end date, no start"
        r = ReadingFactory(end_date=make_date('2017-02-01'),
                           end_granularity=4)
        self.assertEqual(reading_dates(r),
            'Finished in <time datetime="2017-02">Feb&nbsp;2017</time>')

    def test_end_y(self):
        "Year-based end date, no start"
        r = ReadingFactory(end_date=make_date('2017-02-01'),
                           end_granularity=6)
        self.assertEqual(reading_dates(r),
            'Finished in <time datetime="2017">2017</time>')


    # Only a start_date.

    def test_start_ymd(self):
        "Complete start date, no end"
        r = ReadingFactory(start_date=make_date('2017-02-01'),
                           start_granularity=3)
        self.assertEqual(reading_dates(r),
            'Started on <time datetime="2017-02-01">1&nbsp;Feb&nbsp;2017</time>')

    def test_start_ym(self):
        "Month-based start date, no end"
        r = ReadingFactory(start_date=make_date('2017-02-01'),
                           start_granularity=4)
        self.assertEqual(reading_dates(r),
            'Started in <time datetime="2017-02">Feb&nbsp;2017</time>')

    def test_start_y(self):
        "Year-based start date, no end"
        r = ReadingFactory(start_date=make_date('2017-02-01'),
                           start_granularity=6)
        self.assertEqual(reading_dates(r),
            'Started in <time datetime="2017">2017</time>')


class InProgressPublicationsTestCase(TestCase):

    def test_queryset(self):
        "It should return in-progress publications."
        in_progress = ReadingFactory(
                start_date=make_date('2017-02-10'),
            )
        finished = ReadingFactory(
                start_date=make_date('2017-01-15'),
                end_date=make_date('2017-01-28'),
            )
        qs = in_progress_publications()
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0], in_progress.publication)


class RecentEventsTestCase(TestCase):

    def test_queryset(self):
        "It should return 10 recent events by default."
        MovieEventFactory.create_batch(6, date=make_date('2017-02-10'))
        ConcertFactory.create_batch(6,    date=make_date('2017-02-12'))
        qs = recent_events()
        self.assertEqual(len(qs), 10)
        self.assertEqual(qs[5].event_kind, 'concert')
        self.assertEqual(qs[6].event_kind, 'movie')

    def test_queryset_num(self):
        "It should return the number of events requested."
        ConcertFactory.create_batch(6, date=make_date('2017-02-12'))
        qs = recent_events(5)
        self.assertEqual(len(qs), 5)


