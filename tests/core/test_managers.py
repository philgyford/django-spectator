# coding: utf-8
from django.test import override_settings, TestCase

from .. import make_date
from spectator.core.factories import *
from spectator.reading.factories import *
from spectator.core.models import Creator


# The dates make no difference to these tests, so just define one:
d = make_date('2017-02-15')


class CreatorManagerByPublicationsTestCase(TestCase):
    """
    Testing the CreatorManager.by_publications() method.
    """

    def test_has_count_field(self):
        pub = PublicationFactory()
        PublicationRoleFactory(publication=pub)
        ReadingFactory(publication=pub, start_date=d, end_date=d)

        creators = Creator.objects.by_publications()

        self.assertEqual(len(creators), 1)
        self.assertTrue(hasattr(creators[0], 'num_publications'))
        self.assertEqual(creators[0].num_publications, 1)

    def test_does_not_count_unread_publicatios(self):
        unread_pub = PublicationFactory()
        PublicationRoleFactory(publication=unread_pub)

        read_pub = PublicationFactory()
        PublicationRoleFactory(publication=read_pub)

        ReadingFactory(publication=read_pub, start_date=d, end_date=d)

        creators = Creator.objects.by_publications()

        self.assertEqual(creators[0].num_publications, 1)

    def test_sorts_by_name(self):
        "If counts are equal."
        terry = IndividualCreatorFactory(name='Terry')
        bob = IndividualCreatorFactory(name='Bob')

        pub1 = PublicationFactory()
        PublicationRoleFactory(publication=pub1, creator=terry)
        pub2 = PublicationFactory()
        PublicationRoleFactory(publication=pub2, creator=bob)

        ReadingFactory(publication=pub2, start_date=d, end_date=d)
        ReadingFactory(publication=pub1, start_date=d, end_date=d)

        creators = Creator.objects.by_publications()

        self.assertEqual(len(creators), 2)
        self.assertEqual(creators[0], bob)
        self.assertEqual(creators[1], terry)

    def test_counts_joint_publications(self):
        "If one publication has multiple authors, it counts them correctly."
        bob = IndividualCreatorFactory()
        terry = IndividualCreatorFactory()

        # bob has one solo publication:
        pub_bob = PublicationFactory()
        PublicationRoleFactory(publication=pub_bob, creator=bob)

        # terry has two solo publications:
        pub_terry1 = PublicationFactory()
        pub_terry2 = PublicationFactory()
        PublicationRoleFactory(publication=pub_terry1, creator=terry)
        PublicationRoleFactory(publication=pub_terry2, creator=terry)

        # Both bob and terry are involved in this pub:
        pub_bob_terry = PublicationFactory()
        PublicationRoleFactory(publication=pub_bob_terry, creator=bob)
        PublicationRoleFactory(publication=pub_bob_terry, creator=terry)

        # One reading each for all of the above publications.
        ReadingFactory(publication=pub_bob, start_date=d, end_date=d)
        ReadingFactory(publication=pub_terry1, start_date=d, end_date=d)
        ReadingFactory(publication=pub_terry2, start_date=d, end_date=d)
        ReadingFactory(publication=pub_bob_terry, start_date=d, end_date=d)

        creators = Creator.objects.by_publications()

        self.assertEqual(len(creators), 2)

        self.assertEqual(creators[0], terry) # 2 solo, 1 joint
        self.assertEqual(creators[0].num_publications, 3)

        self.assertEqual(creators[1], bob) # 1 solo, 1 joint
        self.assertEqual(creators[1].num_publications, 2)


class CreatorManagerByReadingsTestCase(TestCase):
    """
    Testing the CreatorManager.by_readings() method.
    """

    def test_has_count_field(self):
        pub = PublicationFactory()
        PublicationRoleFactory(publication=pub)
        ReadingFactory(publication=pub, start_date=d, end_date=d)

        creators = Creator.objects.by_readings()

        self.assertTrue(hasattr(creators[0], 'num_readings'))
        self.assertEqual(creators[0].num_readings, 1)

    def test_counts_readings(self):
        "Not just publications"
        pub = PublicationFactory()
        PublicationRoleFactory(publication=pub)
        ReadingFactory(publication=pub, start_date=d, end_date=d)
        ReadingFactory(publication=pub, start_date=d, end_date=d)

        creators = Creator.objects.by_readings()

        self.assertEqual(creators[0].num_readings, 2)

    def test_does_not_count_unread_publicatios(self):
        unread_pub = PublicationFactory()
        PublicationRoleFactory(publication=unread_pub)

        read_pub = PublicationFactory()
        PublicationRoleFactory(publication=read_pub)

        ReadingFactory(publication=read_pub, start_date=d, end_date=d)
        ReadingFactory(publication=read_pub, start_date=d, end_date=d)

        creators = Creator.objects.by_readings()

        self.assertEqual(creators[0].num_readings, 2)

    def test_sorts_by_name(self):
        "If counts are equal."
        terry = IndividualCreatorFactory(name='Terry')
        bob = IndividualCreatorFactory(name='Bob')

        pub1 = PublicationFactory()
        PublicationRoleFactory(publication=pub1, creator=terry)
        pub2 = PublicationFactory()
        PublicationRoleFactory(publication=pub2, creator=bob)

        ReadingFactory(publication=pub2, start_date=d, end_date=d)
        ReadingFactory(publication=pub1, start_date=d, end_date=d)

        creators = Creator.objects.by_readings()

        self.assertEqual(len(creators), 2)
        self.assertEqual(creators[0], bob)
        self.assertEqual(creators[1], terry)
