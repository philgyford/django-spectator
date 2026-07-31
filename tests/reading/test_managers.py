from datetime import date

from django.test import TestCase
from freezegun import freeze_time

from spectator.reading.factories import PublicationFactory, ReadingFactory
from spectator.reading.models import Publication, Reading
from tests import make_date, make_datetime


class PublicationManagersTestCase(TestCase):
    "Testing the various get_queryset() methods for different managers"

    def setUp(self):
        self.unread_pub = PublicationFactory()

        self.read_pub = PublicationFactory()
        ReadingFactory(
            publication=self.read_pub,
            start_date=make_date("2017-02-15"),
            end_date=make_date("2017-02-28"),
        )

        # Has been read once but is being read again:
        self.in_progress_pub = PublicationFactory()
        ReadingFactory(
            publication=self.in_progress_pub,
            start_date=make_date("2017-02-15"),
            end_date=make_date("2017-02-28"),
        )
        ReadingFactory(
            publication=self.in_progress_pub, start_date=make_date("2017-02-15")
        )

    def test_default_manager(self):
        "Should return all publications, no matter their reading state."
        pubs = Publication.objects.all()
        self.assertEqual(len(pubs), 3)

    def test_in_progress_manager(self):
        "Should only return started-but-not-finished Publications."
        pubs = Publication.in_progress_objects.all()
        self.assertEqual(len(pubs), 1)
        self.assertEqual(pubs[0], self.in_progress_pub)

    def test_in_progress_manager_ordering(self):
        "Should be ordered by reading start_date ASC."
        earliest_in_progress_pub = PublicationFactory()
        ReadingFactory(
            publication=earliest_in_progress_pub, start_date=make_date("2017-02-14")
        )
        latest_in_progress_pub = PublicationFactory()
        ReadingFactory(
            publication=latest_in_progress_pub, start_date=make_date("2017-02-16")
        )
        pubs = Publication.in_progress_objects.all()
        self.assertEqual(len(pubs), 3)
        self.assertEqual(pubs[0], earliest_in_progress_pub)
        self.assertEqual(pubs[1], self.in_progress_pub)
        self.assertEqual(pubs[2], latest_in_progress_pub)

    def test_unread_manager(self):
        "Should only return unread Publications."
        pubs = Publication.unread_objects.all()
        self.assertEqual(len(pubs), 1)
        self.assertEqual(pubs[0], self.unread_pub)


@freeze_time("2026-07-15 12:00:00")
class UnreadPublicationsManagerGetCountsForDatesTestCase(TestCase):
    "Testing the UnreadPublicationsManager.get_counts_for_dates() method only"

    def test_past_readings(self):
        "It should not count Pubs with Readings in the past"
        pub = PublicationFactory()
        pub.time_created = make_datetime("2025-01-01 12:00:00")
        pub.save()
        ReadingFactory(
            publication=pub,
            start_date=make_date("2025-01-02"),  # Started before chosen date
            end_date=make_date("2025-01-05"),  # Finished before chosen date
        )
        counts = Publication.unread_objects.get_counts_for_dates([date(2025, 1, 15)])
        self.assertDictEqual(counts, {date(2025, 1, 15): 0})

    def test_in_progress_readings(self):
        "It should not count Pubs with in-progress Readings"
        pub = PublicationFactory()
        pub.time_created = make_datetime("2025-01-01 12:00:00")
        pub.save()
        ReadingFactory(
            publication=pub,
            start_date=make_date("2025-01-02"),  # Started before chosen date
            end_date=make_date("2025-01-20"),  # Finished after chosen date
        )
        counts = Publication.unread_objects.get_counts_for_dates([date(2025, 1, 15)])
        self.assertDictEqual(counts, {date(2025, 1, 15): 0})

    def test_future_readings(self):
        "It should count Pubs that only have future Readings"
        pub = PublicationFactory()
        pub.time_created = make_datetime("2025-01-01 12:00:00")
        pub.save()
        ReadingFactory(
            publication=pub,
            start_date=make_date("2025-01-16"),  # Started after chosen date
            end_date=make_date("2025-01-20"),
        )
        counts = Publication.unread_objects.get_counts_for_dates([date(2025, 1, 15)])
        self.assertDictEqual(counts, {date(2025, 1, 15): 1})

    def test_multiple_past_readings(self):
        "It should not over count Pubs with multiple past Readings"
        # pub = PublicationFactory()
        # pub.time_created = make_datetime("2025-01-01 12:00:00")
        # pub.save()
        # ReadingFactory(
        #     publication=pub,
        #     start_date=make_date("2025-01-02"),
        #     end_date=make_date("2025-01-05"),  # Finished before chosen date
        # )
        # ReadingFactory(
        #     publication=pub,
        #     start_date=make_date("2025-01-06"),
        #     end_date=make_date("2025-01-10"),  # Finished before chosen date
        # )
        # counts = Publication.unread_objects.get_counts_for_dates([date(2025, 1, 15)])
        # self.assertDictEqual(counts, {date(2025, 1, 15): 1})

    def test_past_readings_with_only_end_dates(self):
        "It should not count Pubs with Readings in the past no start date"
        pub = PublicationFactory()
        pub.time_created = make_datetime("2025-01-01 12:00:00")
        pub.save()
        ReadingFactory(
            publication=pub,
            start_date=None,
            end_date=make_date("2025-01-05"),  # Finished before chosen date
        )
        counts = Publication.unread_objects.get_counts_for_dates([date(2025, 1, 15)])
        self.assertDictEqual(counts, {date(2025, 1, 15): 0})

    def test_future_readings_with_only_end_dates(self):
        "It should count Pubs that only have future Readings (with no start date)"
        pub = PublicationFactory()
        pub.time_created = make_datetime("2025-01-01 12:00:00")
        pub.save()
        ReadingFactory(
            publication=pub,
            start_date=None,
            end_date=make_date("2025-01-20"),  # Finished after chosen date
        )
        counts = Publication.unread_objects.get_counts_for_dates([date(2025, 1, 15)])
        self.assertDictEqual(counts, {date(2025, 1, 15): 1})

    def test_no_readings(self):
        "It should count Pubs with no Readings"
        pub = PublicationFactory()
        pub.time_created = make_datetime("2025-01-01 12:00:00")
        pub.save()
        counts = Publication.unread_objects.get_counts_for_dates([date(2025, 1, 15)])
        self.assertDictEqual(counts, {date(2025, 1, 15): 1})

    def test_future_publications(self):
        "It should not count Pubs added after chosen date"
        pub = PublicationFactory()
        pub.time_created = make_datetime("2025-01-16 12:00:00")  # Added after date
        pub.save()
        counts = Publication.unread_objects.get_counts_for_dates([date(2025, 1, 15)])
        self.assertDictEqual(counts, {date(2025, 1, 15): 0})

    def test_multiple_dates(self):
        "It should return counts for multiple supplied dates"
        # Never read
        pub_1 = PublicationFactory()
        pub_1.time_created = make_datetime("2025-02-01 12:00:00")
        pub_1.save()

        # Read after one of
        pub_2 = PublicationFactory()
        pub_2.time_created = make_datetime("2025-03-01 12:00:00")
        pub_2.save()
        ReadingFactory(
            publication=pub_2,
            start_date=make_date("2025-04-15"),
            end_date=make_date("2025-04-20"),
        )

        dates = [
            date(2025, 1, 15),
            date(2025, 2, 15),
            date(2025, 3, 15),
            date(2025, 4, 15),
            date(2025, 5, 15),
        ]
        counts = Publication.unread_objects.get_counts_for_dates(dates)
        expected = {
            date(2025, 1, 15): 0,  # Neither pub exists
            date(2025, 2, 15): 1,  # Only pub_1 exists
            date(2025, 3, 15): 2,  # Both pubs exist and are unread
            date(2025, 4, 15): 1,  # pub_2 has started a Reading
            date(2025, 5, 15): 1,  # pub_2 has finished a Reading
        }
        self.assertDictEqual(counts, expected)

    def test_books_and_periodicals(self):
        "Something"


class ReadingManagersTestCase(TestCase):
    def setUp(self):
        self.in_progress = ReadingFactory(start_date=make_date("2017-02-10"))
        self.reading1 = ReadingFactory(
            start_date=make_date("2017-01-15"), end_date=make_date("2017-01-28")
        )
        self.reading2 = ReadingFactory(
            start_date=make_date("2017-02-15"), end_date=make_date("2017-02-28")
        )

    def test_default_manager(self):
        "EndDateAscendingReadingsManager. A reading that's in progress should be last."
        readings = Reading.objects.all()
        self.assertEqual(readings[0], self.reading1)
        self.assertEqual(readings[1], self.reading2)
        self.assertEqual(readings[2], self.in_progress)

    def test_objects_asc_manager(self):
        """EndDateDescendingReadingsManager. A reading that's in
        progress should be first.
        """
        readings = Reading.objects_desc.all()
        self.assertEqual(readings[0], self.in_progress)
        self.assertEqual(readings[1], self.reading2)
        self.assertEqual(readings[2], self.reading1)
