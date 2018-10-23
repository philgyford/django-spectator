from django.test import TestCase

from .. import make_date
from spectator.reading.factories import PublicationFactory, ReadingFactory

from spectator.reading.utils import annual_reading_counts


class AnnualReadingCountsTestCase(TestCase):

    def setUp(self):
        # Books only in 2015:
        ReadingFactory.create_batch(2,
                        publication=PublicationFactory(kind='book'),
                        end_date=make_date('2015-01-01'))

        # Nothing in 2016.

        # Books and periodicals in 2017:
        ReadingFactory.create_batch(3,
                        publication=PublicationFactory(kind='book'),
                        end_date=make_date('2017-09-01'))
        ReadingFactory.create_batch(2,
                        publication=PublicationFactory(kind='periodical'),
                        end_date=make_date('2017-09-01'))

        # Periodicals only in 2018:
        ReadingFactory.create_batch(2,
                        publication=PublicationFactory(kind='periodical'),
                        end_date=make_date('2018-01-01'))

    def test_default(self):
        "With no argugments"

        result = annual_reading_counts()

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0],
                    {'year': make_date('2015-01-01'),
                     'book': 2, 'periodical': 0,'total': 2})
        self.assertEqual(result[1],
                    {'year': make_date('2017-01-01'),
                    'book': 3, 'periodical': 2, 'total': 5})
        self.assertEqual(result[2],
                    {'year': make_date('2018-01-01'),
                    'book': 0, 'periodical': 2,'total': 2})

    def test_all(self):
        "With kind=all"

        result = annual_reading_counts(kind='all')

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0],
                    {'year': make_date('2015-01-01'),
                     'book': 2, 'periodical': 0,'total': 2})
        self.assertEqual(result[1],
                    {'year': make_date('2017-01-01'),
                    'book': 3, 'periodical': 2,'total': 5})
        self.assertEqual(result[2],
                    {'year': make_date('2018-01-01'),
                    'book': 0, 'periodical': 2,'total': 2})

    def test_book(self):
        "With kind=book"

        result = annual_reading_counts(kind='book')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0],
                    {'year': make_date('2015-01-01'),
                     'book': 2})
        self.assertEqual(result[1],
                    {'year': make_date('2017-01-01'),
                    'book': 3})

    def test_periodical(self):
        "With kind=periodical"

        result = annual_reading_counts(kind='periodical')

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0],
                    {'year': make_date('2017-01-01'),
                    'periodical': 2})
        self.assertEqual(result[1],
                    {'year': make_date('2018-01-01'),
                    'periodical': 2})
