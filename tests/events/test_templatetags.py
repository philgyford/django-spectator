from django.test import TestCase

from .. import make_date
from spectator.events.factories import GigEventFactory, MovieEventFactory
from spectator.events.templatetags.spectator_events import day_events,\
        recent_events


class RecentEventsTestCase(TestCase):

    def test_queryset(self):
        "It should return 10 recent events by default."
        MovieEventFactory.create_batch(6, date=make_date('2017-02-10'))
        GigEventFactory.create_batch(6,    date=make_date('2017-02-12'))
        qs = recent_events()
        self.assertEqual(len(qs), 10)
        self.assertEqual(qs[5].kind, 'gig')
        self.assertEqual(qs[6].kind, 'movie')

    def test_queryset_num(self):
        "It should return the number of events requested."
        GigEventFactory.create_batch(6, date=make_date('2017-02-12'))
        qs = recent_events(5)
        self.assertEqual(len(qs), 5)


class DayEventsTestCase(TestCase):

    def test_queryset(self):
        GigEventFactory(  date=make_date('2017-02-09'))
        MovieEventFactory(date=make_date('2017-02-10'))
        GigEventFactory(  date=make_date('2017-02-10'))
        MovieEventFactory(date=make_date('2017-02-11'))
        qs = day_events(make_date('2017-02-10'))
        self.assertEqual(len(qs), 2)

