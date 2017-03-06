from django.test import TestCase

from . import make_date
from spectator.factories import *
from spectator.models import Publication, Reading


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

    def test_unread_manager(self):
        "Should only return unread Publications."
        pubs = Publication.unread_objects.all()
        self.assertEqual(len(pubs), 1)
        self.assertEqual(pubs[0], self.unread_pub)


class ReadingTestCase(TestCase):

    def test_str(self):
        reading = ReadingFactory(
                publication=PublicationFactory(title='Big Book'),
                start_date=make_date('2017-02-15'),
                end_date=make_date('2017-02-28'),
            )
        self.assertEqual(str(reading), 'Big Book (2017-02-15 to 2017-02-28)')

    def test_ordering(self):
        reading1 = ReadingFactory(
                start_date=make_date('2017-02-15'),
                end_date=make_date('2017-02-28'),
            )
        reading2 = ReadingFactory(
                start_date=make_date('2017-01-15'),
                end_date=make_date('2017-01-28'),
            )
        readings = Reading.objects.all()
        self.assertEqual(readings[0], reading2)
        self.assertEqual(readings[1], reading1)
