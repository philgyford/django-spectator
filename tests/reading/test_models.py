from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

from .. import make_date
from spectator.core.factories import *
from spectator.reading.factories import *
from spectator.reading.models import Publication, Reading


class PublicationRoleTestCase(TestCase):

    def test_str_1(self):
        creator = IndividualCreatorFactory(name='Bill Brown')
        role = PublicationRoleFactory(creator=creator, role_name='')
        self.assertEqual(str(role), 'Bill Brown')

    def test_str_2(self):
        creator = IndividualCreatorFactory(name='Bill Brown')
        role = PublicationRoleFactory(creator=creator, role_name='Editor')
        self.assertEqual(str(role), 'Bill Brown (Editor)')


class PublicationSeriesTestCase(TestCase):

    def test_str(self):
        series = PublicationSeriesFactory(title='The London Review of Books')
        self.assertEqual(str(series), 'The London Review of Books')

    def test_absolute_url(self):
        series = PublicationSeriesFactory(pk=3)
        self.assertEqual(series.get_absolute_url(), '/reading/series/3/')


class PublicationTestCase(TestCase):

    def test_str(self):
        pub = PublicationFactory(title='Aurora')
        self.assertEqual(str(pub), 'Aurora')

    def test_ordering(self):
        "Should order by book title."
        b3 = PublicationFactory(title='Publication C')
        b1 = PublicationFactory(title='Publication A')
        b2 = PublicationFactory(title='Publication B')
        pubs = Publication.objects.all()
        self.assertEqual(pubs[0], b1)
        self.assertEqual(pubs[1], b2)
        self.assertEqual(pubs[2], b3)

    def test_absolute_url(self):
        pub = PublicationFactory(pk=3)
        self.assertEqual(pub.get_absolute_url(), '/reading/publications/3/')

    def test_roles(self):
        "It can have multiple PublicationRoles."
        bob = IndividualCreatorFactory(name='Bob')
        terry = IndividualCreatorFactory(name='Terry')
        pub = PublicationFactory()
        bobs_role = PublicationRoleFactory(publication=pub, creator=bob,
                                        role_name='Editor', role_order=2)
        terrys_role = PublicationRoleFactory(publication=pub, creator=terry,
                                        role_name='Author', role_order=1)
        roles = pub.roles.all()
        self.assertEqual(len(roles), 2)
        self.assertEqual(roles[0], terrys_role)
        self.assertEqual(roles[1], bobs_role)
        self.assertEqual(roles[0].role_name, 'Author')
        self.assertEqual(roles[1].role_name, 'Editor')

    def test_amazon_uk_url(self):
        p = PublicationFactory(isbn_uk='0356500489')
        self.assertEqual(p.amazon_uk_url,
                         'https://www.amazon.co.uk/gp/product/0356500489/')

    def test_amazon_uk_url_none(self):
        p = PublicationFactory(isbn_uk='')
        self.assertEqual(p.amazon_uk_url, '')

    @override_settings(SPECTATOR_AMAZON={'uk': 'foobar-21'})
    def test_amazon_uk_url_affiliate(self):
        p = PublicationFactory(isbn_uk='0356500489')
        self.assertEqual(p.amazon_uk_url,
             'https://www.amazon.co.uk/gp/product/0356500489/?tag=foobar-21')

    def test_amazon_us_url(self):
        p = PublicationFactory(isbn_us='0356500489')
        self.assertEqual(p.amazon_us_url,
                         'https://www.amazon.com/dp/0356500489/')

    def test_amazon_us_url_none(self):
        p = PublicationFactory(isbn_us='')
        self.assertEqual(p.amazon_us_url, '')

    @override_settings(SPECTATOR_AMAZON={'us': 'foobar-20'})
    def test_amazon_us_url_affiliate(self):
        p = PublicationFactory(isbn_us='0356500489')
        self.assertEqual(p.amazon_us_url,
             'https://www.amazon.com/dp/0356500489/?tag=foobar-20')

    def test_amazon_urls(self):
        p = PublicationFactory(isbn_uk='1234567890',
                               isbn_us='3333333333')
        self.assertEqual(p.amazon_urls, [
            {'url': p.amazon_uk_url, 'name': 'Amazon.co.uk', 'country': 'UK'},
            {'url': p.amazon_us_url, 'name': 'Amazon.com', 'country': 'USA'},
        ])

    def test_amazon_urls_none(self):
        p = PublicationFactory(isbn_uk='', isbn_us='')
        self.assertEqual(p.amazon_urls, [])

    def test_has_urls_no(self):
        p = PublicationFactory()
        self.assertFalse(p.has_urls)

    def test_has_urls_official(self):
        p = PublicationFactory(official_url='http://www.example.org')
        self.assertTrue(p.has_urls)

    def test_has_urls_notes(self):
        p = PublicationFactory(notes_url='http://www.example.org')
        self.assertTrue(p.has_urls)

    def test_has_urls_isbn_uk(self):
        p = PublicationFactory(isbn_uk='1234567890')
        self.assertTrue(p.has_urls)

    def test_has_urls_isbn_us(self):
        p = PublicationFactory(isbn_us='1234567890')
        self.assertTrue(p.has_urls)

    def test_get_current_reading(self):
        "It should return the one in-progress Reading."
        p = PublicationFactory()
        in_progress = ReadingFactory(publication=p,
                                    start_date=make_date('2017-02-15'))
        completed = ReadingFactory(publication=p,
                                    start_date=make_date('2017-02-15'),
                                    end_date=make_date('2017-02-28'))
        self.assertEqual(p.get_current_reading(), in_progress)

    def test_get_current_reading_none(self):
        "If there's no in-progress Reading, it should return nothing."
        p = PublicationFactory()
        completed = ReadingFactory(publication=p,
                                    start_date=make_date('2017-02-15'),
                                    end_date=make_date('2017-02-28'))
        self.assertIsNone(p.get_current_reading())


class ReadingTestCase(TestCase):

    def test_str(self):
        reading = ReadingFactory(
                publication=PublicationFactory(title='Big Book'),
                start_date=make_date('2017-02-15'),
                end_date=make_date('2017-02-28'),
            )
        self.assertEqual(str(reading), 'Big Book (2017-02-15 to 2017-02-28)')

    def test_clean_error(self):
        "It won't accept an end_date before a start_date."
        reading = ReadingFactory(
                start_date=make_date('2017-02-15'),
                end_date=make_date('2016-02-28'),
            )
        with self.assertRaises(ValidationError):
            reading.clean()

    def test_clean_no_error(self):
        reading = ReadingFactory(
                start_date=make_date('2016-02-28'),
                end_date=make_date('2017-02-15'),
            )
        try:
            reading.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly.")

