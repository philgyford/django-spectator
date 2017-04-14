from django.test import TestCase

from .. import make_date
from spectator.events.factories import GigEventFactory, MovieEventFactory
from spectator.events.models import Event
from spectator.events.templatetags.spectator_events import\
        day_events, day_events_card, event_list_breadcrumbs, event_list_tabs,\
        events_years, events_years_card,\
        recent_events, recent_events_card


class EventListBreadcrumbsTestCase(TestCase):

    def test_result(self):
        result = event_list_breadcrumbs('gig')
        self.assertEqual(result['current_kind'], 'gig')
        self.assertEqual(
            sorted(result['event_kinds']),
            sorted(Event.get_kinds())
        )
        self.assertEqual(
            sorted(result['event_kinds_data'].keys()),
            sorted(Event.get_kinds_data().keys())
        )


class EventListTabsTestCase(TestCase):

    def test_result(self):
        counts = {'all': 30, 'gig': 12, 'movie': 18,}
        result = event_list_tabs(counts, 'gig')
        self.assertEqual(result['counts'], counts)
        self.assertEqual(result['current_kind'], 'gig')
        self.assertEqual(
            sorted(result['event_kinds']),
            sorted(Event.get_kinds())
        )
        self.assertEqual(
            sorted(result['event_kinds_data'].keys()),
            sorted(Event.get_kinds_data().keys())
        )


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


class RecentEventsCardTestCase(TestCase):

    def test_result(self):
        GigEventFactory.create_batch(6, date=make_date('2017-02-12'))
        result = recent_events_card(5)
        self.assertEqual(result['card_title'], 'Recent events')
        self.assertEqual(len(result['event_list']), 5)


class DayEventsTestCase(TestCase):

    def test_queryset(self):
        GigEventFactory(  date=make_date('2017-02-09'))
        MovieEventFactory(date=make_date('2017-02-10'))
        GigEventFactory(  date=make_date('2017-02-10'))
        MovieEventFactory(date=make_date('2017-02-11'))
        qs = day_events(make_date('2017-02-10'))
        self.assertEqual(len(qs), 2)


class DayEventsCardTestCase(TestCase):

    def test_result(self):
        GigEventFactory(  date=make_date('2017-02-09'))
        MovieEventFactory(date=make_date('2017-02-10'))
        GigEventFactory(  date=make_date('2017-02-10'))
        MovieEventFactory(date=make_date('2017-02-11'))
        result = day_events_card(make_date('2017-02-10'))
        self.assertEqual(result['card_title'], 'Events on 10 Feb 2017')
        self.assertEqual(len(result['event_list']), 2)


class EventsYearsTestCase(TestCase):

    def test_result(self):
        GigEventFactory(  date=make_date('2017-02-09'))
        MovieEventFactory(date=make_date('2017-02-10'))
        GigEventFactory(  date=make_date('2015-02-09'))
        result = events_years()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], make_date('2015-01-01'))
        self.assertEqual(result[1], make_date('2017-01-01'))


class EventsYearsCardTestCase(TestCase):

    def test_result(self):
        GigEventFactory(  date=make_date('2017-02-09'))
        MovieEventFactory(date=make_date('2017-02-10'))
        GigEventFactory(  date=make_date('2015-02-09'))
        result = events_years_card(make_date('2017-01-01'))
        self.assertEqual(result['current_year'], make_date('2017-01-01'))
        self.assertEqual(len(result['years']), 2)
        self.assertEqual(result['years'][0], make_date('2015-01-01'))
        self.assertEqual(result['years'][1], make_date('2017-01-01'))


