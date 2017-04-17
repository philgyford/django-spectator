from django.test import TestCase

from .. import make_date
from spectator.reading.factories import PublicationFactory, ReadingFactory
from spectator.reading.templatetags.spectator_reading import day_publications,\
        in_progress_publications, reading_dates, reading_years


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


class DayPublicationsTestCase(TestCase):

    def test_ended_readings(self):
        "It returns publications whose ended readings were around the date"
        pub1 = PublicationFactory()
        pub2 = PublicationFactory()
        # pub1 started before and ended after the date:
        ReadingFactory(publication=pub1,
                        start_date=make_date('2017-02-10'),
                        end_date=make_date('2017-02-20')
                    )
        # pub2 was over before the date:
        ReadingFactory(publication=pub2,
                        start_date=make_date('2017-01-01'),
                        end_date=make_date('2017-01-10')
                    )
        qs = day_publications(make_date('2017-02-15'))
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0], pub1)

    def test_in_progress_readings(self):
        "It returns publications that were still in progress on the date."
        pub1 = PublicationFactory()
        pub2 = PublicationFactory()
        # pub1 started before the date:
        ReadingFactory(publication=pub1,
                        start_date=make_date('2017-02-10'),
                        end_date=None
                    )
        # pub2 started after the date:
        ReadingFactory(publication=pub2,
                        start_date=make_date('2017-03-01'),
                        end_date=None
                    )
        qs = day_publications(make_date('2017-02-15'))
        self.assertEqual(len(qs), 1)
        self.assertEqual(qs[0], pub1)


class ReadingYearsTestCase(TestCase):

    def test_queryset(self):
        ReadingFactory(start_date=make_date('2015-02-10'),
                        end_date=make_date('2015-02-15')
                    )
        ReadingFactory(start_date=make_date('2017-02-10'),
                        end_date=make_date('2017-02-15')
                    )
        ReadingFactory(start_date=make_date('2017-03-10'),
                        end_date=make_date('2017-03-15')
                    )
        qs = reading_years()
        self.assertEqual(len(qs), 2)
        self.assertEqual(qs[0], make_date('2015-01-01'))
        self.assertEqual(qs[1], make_date('2017-01-01'))


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


