# coding: utf-8
from django.test import override_settings, TestCase

from spectator.events.factories import *
from spectator.events.models import Venue, Work


class VenueManagerByVisitsTestCase(TestCase):
    """
    Testing the VenueManager.by_visits() method.
    """

    def test_has_count_field(self):
        MiscEventFactory(venue=VenueFactory())

        venues = Venue.objects.by_visits()

        self.assertEqual(len(venues), 1)
        self.assertTrue(hasattr(venues[0], 'num_visits'))
        self.assertEqual(venues[0].num_visits, 1)

    def test_sorts_by_num_visits(self):
        v1 = VenueFactory()
        v2 = VenueFactory()
        v3 = VenueFactory()

        MiscEventFactory(venue=v1)
        GigEventFactory(venue=v1)

        GigEventFactory(venue=v2)

        MiscEventFactory(venue=v3)
        GigEventFactory(venue=v3)
        DanceEventFactory(venue=v3)

        venues = Venue.objects.by_visits()

        self.assertEqual(len(venues), 3)
        self.assertEqual(venues[0], v3)
        self.assertEqual(venues[0].num_visits, 3)
        self.assertEqual(venues[1], v1)
        self.assertEqual(venues[1].num_visits, 2)
        self.assertEqual(venues[2], v2)
        self.assertEqual(venues[2].num_visits, 1)

    def test_sorts_by_name(self):
        "If num_visits is equal"
        v1 = VenueFactory(name='B')
        v2 = VenueFactory(name='C')
        v3 = VenueFactory(name='A')

        MiscEventFactory(venue=v1)
        MiscEventFactory(venue=v2)
        MiscEventFactory(venue=v3)

        venues = Venue.objects.by_visits()

        self.assertEqual(len(venues), 3)
        self.assertEqual(venues[0], v3)
        self.assertEqual(venues[1], v1)
        self.assertEqual(venues[2], v2)

    def test_filters_by_kind(self):
        v = VenueFactory()

        ComedyEventFactory(venue=v)
        ComedyEventFactory(venue=v)
        DanceEventFactory(venue=v)

        venues = Venue.objects.by_visits(event_kind='comedy')

        self.assertEqual(venues[0].num_visits, 2)


class WorkManagerByVisitsTestCase(TestCase):
    """
    Testing the WorkManager.by_views() method.
    """

    def test_has_count_field(self):
        WorkSelectionFactory(event=CinemaEventFactory(), work=MovieFactory())

        works = Work.objects.by_views()

        self.assertEqual(len(works), 1)
        self.assertTrue(hasattr(works[0], 'num_views'))
        self.assertEqual(works[0].num_views, 1)

    def test_sorts_by_num_views(self):
        play = PlayFactory()
        WorkSelectionFactory(event=TheatreEventFactory(), work=play)
        WorkSelectionFactory(event=TheatreEventFactory(), work=play)

        cw = ClassicalWorkFactory()
        WorkSelectionFactory(event=TheatreEventFactory(), work=cw)

        movie = MovieFactory()
        WorkSelectionFactory(event=CinemaEventFactory(), work=movie)
        WorkSelectionFactory(event=CinemaEventFactory(), work=movie)
        WorkSelectionFactory(event=CinemaEventFactory(), work=movie)

        works = Work.objects.by_views()

        self.assertEqual(len(works), 3)
        self.assertEqual(works[0], movie)
        self.assertEqual(works[0].num_views, 3)
        self.assertEqual(works[1], play)
        self.assertEqual(works[1].num_views, 2)
        self.assertEqual(works[2], cw)
        self.assertEqual(works[2].num_views, 1)

    def test_sorts_by_title(self):
        "If num_views is equal"
        m1 = MovieFactory(title='B')
        m2 = MovieFactory(title='C')
        m3 = MovieFactory(title='A')
        WorkSelectionFactory(event=CinemaEventFactory(), work=m1)
        WorkSelectionFactory(event=CinemaEventFactory(), work=m2)
        WorkSelectionFactory(event=CinemaEventFactory(), work=m3)

        works = Work.objects.by_views()

        self.assertEqual(works[0], m3)
        self.assertEqual(works[1], m1)
        self.assertEqual(works[2], m2)

    def test_filters_by_kind(self):
        movie = MovieFactory()
        play = PlayFactory()
        WorkSelectionFactory(event=CinemaEventFactory(), work=movie)
        WorkSelectionFactory(event=TheatreEventFactory(), work=play)

        works = Work.objects.by_views(kind='movie')

        self.assertEqual(len(works), 1)
        self.assertEqual(works[0], movie)
