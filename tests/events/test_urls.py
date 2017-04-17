from django.test import TestCase
try:
    # Django >= 1.10
    from django.urls import resolve, reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import resolve, reverse

from .. import make_date
from spectator.events import views
from spectator.events.factories import GigEventFactory


class EventsUrlsTestCase(TestCase):

    # HOME

    def test_events_home_url(self):
        self.assertEqual(reverse('spectator:events:home'), '/events/')

    def test_events_home_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/').func.__name__,
                         views.EventListView.__name__)

    # VENUES

    def test_venue_list_url(self):
        self.assertEqual(reverse('spectator:events:venue_list'), '/events/venues/')

    def test_venue_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/venues/').func.__name__,
                         views.VenueListView.__name__)

    def test_venue_detail_url(self):
        self.assertEqual(reverse('spectator:events:venue_detail', kwargs={'pk':34,}),
                        '/events/venues/34/')

    def test_venue_detail_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/venues/34/').func.__name__,
                         views.VenueDetailView.__name__)

    # YEARS

    def test_event_year_archive_url(self):
        GigEventFactory(date=make_date('2017-02-15'))
        self.assertEqual(
                reverse('spectator:events:event_year_archive', kwargs={'year': 2017}),
                    '/events/2017/')

    def test_event_year_archive_view(self):
        "Should use the correct view."
        GigEventFactory(date=('2017-02-15'))
        self.assertEqual(resolve('/events/2017/').func.__name__,
                         views.EventYearArchiveView.__name__)

    # EVENTS

    def test_event_list_url(self):
        self.assertEqual(
                reverse('spectator:events:event_list', kwargs={'kind_slug': 'gigs'}),
            '/events/gigs/')

    def test_event_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/gigs/').func.__name__,
                         views.EventListView.__name__)

    def test_event_detail_url(self):
        self.assertEqual(
                reverse('spectator:events:event_detail',
                kwargs={'kind_slug': 'gigs', 'pk':34,}),
            '/events/gigs/34/')

    def test_event_detail_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/gigs/34/').func.__name__,
                         views.EventDetailView.__name__)

