from django.test import TestCase
try:
    # Django >= 1.10
    from django.urls import resolve, reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import resolve, reverse

from .. import make_date
from spectator.events import views
from spectator.factories import ConcertFactory


class EventsUrlsTestCase(TestCase):

    # Event lists

    def test_events_home_url(self):
        self.assertEqual(reverse('spectator:events_home'), '/events/')

    def test_events_home_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/').func.__name__,
                         views.EventsHomeView.__name__)

    # CONCERTS

    def test_concert_list_url(self):
        self.assertEqual(reverse('spectator:concert_list'), '/events/concerts/')

    def test_concert_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/concerts/').func.__name__,
                         views.ConcertListView.__name__)

    def test_concertevent_list_url(self):
        self.assertEqual(reverse('spectator:concert_visits'),
                        '/events/concerts/visits/')

    def test_concertevent_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/concerts/visits/').func.__name__,
                         views.ConcertEventListView.__name__)

    def test_concert_detail_url(self):
        self.assertEqual(reverse('spectator:concert_detail', kwargs={'pk':34,}),
                        '/events/concerts/34/')

    def test_concert_detail_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/concerts/34/').func.__name__,
                         views.ConcertDetailView.__name__)

    # MOVIES

    def test_movie_list_url(self):
        self.assertEqual(reverse('spectator:movie_list'), '/events/movies/')

    def test_movie_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/movies/').func.__name__,
                         views.MovieListView.__name__)

    def test_movieevent_list_url(self):
        self.assertEqual(reverse('spectator:movie_visits'),
                         '/events/movies/visits/')

    def test_movieevent_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/movies/visits/').func.__name__,
                         views.MovieEventListView.__name__)

    def test_movie_detail_url(self):
        self.assertEqual(reverse('spectator:movie_detail', kwargs={'pk':34,}),
                        '/events/movies/34/')

    def test_movie_detail_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/movies/34/').func.__name__,
                         views.MovieDetailView.__name__)

    # PLAYS

    def test_play_list_url(self):
        self.assertEqual(reverse('spectator:play_list'), '/events/plays/')

    def test_play_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/plays/').func.__name__,
                         views.PlayListView.__name__)

    def test_playproductioneventevent_list_url(self):
        self.assertEqual(reverse('spectator:play_visits'),
                         '/events/plays/visits/')

    def test_playproductionevent_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/plays/visits/').func.__name__,
                         views.PlayProductionEventListView.__name__)

    def test_play_detail_url(self):
        self.assertEqual(reverse('spectator:play_detail', kwargs={'pk':34,}),
                        '/events/plays/34/')

    def test_play_detail_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/plays/34/').func.__name__,
                         views.PlayDetailView.__name__)

    # MISCEVENTS

    def test_miscevent_list_url(self):
        self.assertEqual(reverse('spectator:miscevent_list'), '/events/misc/')

    def test_miscevent_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/misc/').func.__name__,
                         views.MiscEventListView.__name__)

    def test_misceventevent_list_url(self):
        self.assertEqual(reverse('spectator:miscevent_visits'),
                        '/events/misc/visits/')

    def test_misceventevent_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/misc/visits/').func.__name__,
                         views.MiscEventVisitListView.__name__)

    def test_miscevent_detail_url(self):
        self.assertEqual(reverse('spectator:miscevent_detail', kwargs={'pk':34,}),
                        '/events/misc/34/')

    def test_miscevent_detail_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/misc/34/').func.__name__,
                         views.MiscEventDetailView.__name__)

    # VENUES

    def test_venue_list_url(self):
        self.assertEqual(reverse('spectator:venue_list'), '/events/venues/')

    def test_venue_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/venues/').func.__name__,
                         views.VenueListView.__name__)

    def test_venue_detail_url(self):
        self.assertEqual(reverse('spectator:venue_detail', kwargs={'pk':34,}),
                        '/events/venues/34/')

    def test_venue_detail_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/events/venues/34/').func.__name__,
                         views.VenueDetailView.__name__)

    # OTHER

    def test_event_year_archive_url(self):
        ConcertFactory(date=make_date('2017-02-15'))
        self.assertEqual(
            reverse('spectator:event_year_archive', kwargs={'year': 2017}),
                    '/events/2017/')

    def test_event_year_archive_view(self):
        "Should use the correct view."
        ConcertFactory(date=('2017-02-15'))
        self.assertEqual(resolve('/events/2017/').func.__name__,
                         views.EventYearArchiveView.__name__)
