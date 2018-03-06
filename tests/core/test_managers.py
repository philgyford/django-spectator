# coding: utf-8
from django.test import override_settings, TestCase

from .. import make_date
from spectator.core.factories import *
from spectator.events.factories import *
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


class CreatorManagerByEventsTestCase(TestCase):

    def test_has_count_field(self):
        ev = ComedyEventFactory()
        EventRoleFactory(event=ev)

        creators = Creator.objects.by_events()

        self.assertTrue(hasattr(creators[0], 'num_events'))
        self.assertEqual(creators[0].num_events, 1)

    def test_counts_events(self):
        c = IndividualCreatorFactory()
        ev1 = ComedyEventFactory()
        ev2 = GigEventFactory()
        EventRoleFactory(creator=c, event=ev1)
        EventRoleFactory(creator=c, event=ev2)

        creators = Creator.objects.by_events()

        self.assertEqual(creators[0].num_events, 2)

    def test_sorts_by_num_events(self):
        bob = IndividualCreatorFactory()
        terry = IndividualCreatorFactory()
        ev1 = ComedyEventFactory()
        ev2 = GigEventFactory()

        # Both are involved in event 1:
        EventRoleFactory(creator=terry, event=ev1)
        EventRoleFactory(creator=bob, event=ev1)

        # Only bob is involved in event 2:
        EventRoleFactory(creator=bob, event=ev2)

        creators = Creator.objects.by_events()

        self.assertEqual(len(creators), 2)
        self.assertEqual(creators[0], bob)
        self.assertEqual(creators[0].num_events, 2)
        self.assertEqual(creators[1], terry)
        self.assertEqual(creators[1].num_events, 1)

    def test_sorts_by_name(self):
        "If counts are equal"
        terry = IndividualCreatorFactory(name='terry')
        bob = IndividualCreatorFactory(name='bob')
        ev2 = GigEventFactory()
        ev1 = ComedyEventFactory()

        EventRoleFactory(creator=terry, event=ev1)
        EventRoleFactory(creator=bob, event=ev2)

        creators = Creator.objects.by_events()

        self.assertEqual(len(creators), 2)
        self.assertEqual(creators[0], bob)
        self.assertEqual(creators[1], terry)

    def filters_by_kind(self):
        "If supplied with a `kind` argument."
        c = IndividualCreatorFactory()

        gig = GigEventFactory()
        comedy = ComedyEventFactory()
        cinema = CinemaEventFactory()

        EventRoleFactory(creator=c, event=gig)
        EventRoleFactory(creator=c, event=comedy)
        EventRoleFactory(creator=c, event=cinema)

        creators = Creator.objects.by_events(kind='gig')

        # Should only count the 'gig' event:
        self.assertEqual(creators[0].num_events, 1)
