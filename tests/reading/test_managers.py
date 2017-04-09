from django.test import TestCase

from .. import make_date
from spectator.reading.factories import *
from spectator.reading.models import Publication, Reading


class PublicationManagersTestCase(TestCase):

    def setUp(self):
        self.unread_pub = PublicationFactory()

        self.read_pub = PublicationFactory()
        ReadingFactory(publication=self.read_pub,
                        start_date=make_date('2017-02-15'),
                        end_date=make_date('2017-02-28'),
                    )

        # Has been read once but is being read again:
        self.in_progress_pub = PublicationFactory()
        ReadingFactory(publication=self.in_progress_pub,
                        start_date=make_date('2017-02-15'),
                        end_date=make_date('2017-02-28'),
                    )
        ReadingFactory(publication=self.in_progress_pub,
                        start_date=make_date('2017-02-15'),
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
        ReadingFactory(publication=earliest_in_progress_pub,
                        start_date=make_date('2017-02-14'),
                    )
        latest_in_progress_pub = PublicationFactory()
        ReadingFactory(publication=latest_in_progress_pub,
                        start_date=make_date('2017-02-16'),
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


class ReadingManagersTestCase(TestCase):

    def setUp(self):
        self.in_progress = ReadingFactory(
                start_date=make_date('2017-02-10'),
            )
        self.reading1 = ReadingFactory(
                start_date=make_date('2017-01-15'),
                end_date=make_date('2017-01-28'),
            )
        self.reading2 = ReadingFactory(
                start_date=make_date('2017-02-15'),
                end_date=make_date('2017-02-28'),
            )

    def test_default_manager(self):
        "EndDateAscendingReadingsManager. A reading that's in progress should be last."
        readings = Reading.objects.all()
        self.assertEqual(readings[0], self.reading1)
        self.assertEqual(readings[1], self.reading2)
        self.assertEqual(readings[2], self.in_progress)

    def test_objects_asc_manager(self):
        "EndDateDescendingReadingsManager. A reading that's in progress should be first."
        readings = Reading.objects_desc.all()
        self.assertEqual(readings[0], self.in_progress)
        self.assertEqual(readings[1], self.reading2)
        self.assertEqual(readings[2], self.reading1)

