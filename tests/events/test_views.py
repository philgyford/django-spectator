from django.conf import settings
from django.http.response import Http404
from django.test import override_settings

from .. import make_date
from ..core.test_views import ViewTestCase
from spectator.events import views
from spectator.events.factories import ConcertFactory, MovieFactory,\
        MovieEventFactory, PlayFactory, PlayProductionEventFactory,\
        MiscEventFactory, VenueFactory


class EventListViewTestCase(ViewTestCase):
    "Testing some of the aspects of the parent class."

    def test_ancestor(self):
        self.assertTrue(issubclass(views.EventListView,
                                   views.PaginatedListView))

    def test_context_counts(self):
        ConcertFactory.create_batch(5)
        MovieEventFactory.create_batch(4)
        PlayProductionEventFactory.create_batch(3)
        MiscEventFactory.create_batch(2)
        response = views.EventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_count', context)
        self.assertEqual(context['event_count'], 14)
        self.assertIn('concert_count', context)
        self.assertEqual(context['concert_count'], 5)
        self.assertIn('movieevent_count', context)
        self.assertEqual(context['movieevent_count'], 4)
        self.assertIn('playproductionevent_count', context)
        self.assertEqual(context['playproductionevent_count'], 3)
        self.assertIn('miscevent_count', context)
        self.assertEqual(context['miscevent_count'], 2)


class EventsHomeViewTestCase(ViewTestCase):

    def test_ancestor(self):
        self.assertTrue(issubclass(views.EventsHomeView, views.EventListView))

    def test_response_200(self):
        "It should respond with 200."
        response = views.EventsHomeView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.EventsHomeView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/event_list.html')

    def test_context_event_kind(self):
        response = views.EventsHomeView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], 'event')

    def test_context_events_list(self):
        "It should have the latest events, of all kinds, in the context."
        movie = MovieEventFactory(        date=make_date('2017-02-10'))
        play = PlayProductionEventFactory(date=make_date('2017-02-09'))
        concert = ConcertFactory(         date=make_date('2017-02-12'))
        miscevent = MiscEventFactory(     date=make_date('2017-02-05'))
        response = views.EventsHomeView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 4)
        self.assertEqual(context['event_list'][0], concert)
        self.assertEqual(context['event_list'][1], movie)
        self.assertEqual(context['event_list'][2], play)
        self.assertEqual(context['event_list'][3], miscevent)


class ConcertEventListViewTestCase(ViewTestCase):

    def test_ancestor(self):
        self.assertTrue(issubclass(views.ConcertEventListView,
                                   views.EventListView))

    def test_response_200(self):
        "It should respond with 200."
        response = views.ConcertEventListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.ConcertEventListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/event_list.html')

    def test_context_event_kind(self):
        response = views.ConcertEventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], 'concert')

    def test_context_events_list(self):
        "It should have the latest Concert events in the context."
        movie = MovieEventFactory(date=make_date('2017-02-10'))
        concert1 = ConcertFactory(date=make_date('2017-02-09'))
        concert2 = ConcertFactory(date=make_date('2017-02-12'))
        response = views.ConcertEventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 2)
        self.assertEqual(context['event_list'][0], concert2)
        self.assertEqual(context['event_list'][1], concert1)


class MovieEventListViewTestCase(ViewTestCase):

    def test_ancestor(self):
        self.assertTrue(issubclass(views.MovieEventListView,
                                   views.EventListView))

    def test_response_200(self):
        "It should respond with 200."
        response = views.MovieEventListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.MovieEventListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/event_list.html')

    def test_context_event_kind(self):
        response = views.MovieEventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], 'movie')

    def test_context_events_list(self):
        "It should have the latest Movie events in the context."
        concert = ConcertFactory(date=make_date('2017-02-10'))
        movie1 = MovieEventFactory(date=make_date('2017-02-09'))
        movie2 = MovieEventFactory(date=make_date('2017-02-12'))
        response = views.MovieEventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 2)
        self.assertEqual(context['event_list'][0], movie2)
        self.assertEqual(context['event_list'][1], movie1)


class PlayProductionEventListViewTestCase(ViewTestCase):

    def test_ancestor(self):
        self.assertTrue(issubclass(views.PlayProductionEventListView,
                                   views.EventListView))

    def test_response_200(self):
        "It should respond with 200."
        response = views.PlayProductionEventListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.PlayProductionEventListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/event_list.html')

    def test_context_event_kind(self):
        response = views.PlayProductionEventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], 'play')

    def test_context_events_list(self):
        "It should have the latest PlayProduction events in the context."
        concert = ConcertFactory(date=make_date('2017-02-10'))
        playproduction1 = PlayProductionEventFactory(
                                 date=make_date('2017-02-09'))
        playproduction2 = PlayProductionEventFactory(
                                 date=make_date('2017-02-12'))
        response = views.PlayProductionEventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 2)
        self.assertEqual(context['event_list'][0], playproduction2)
        self.assertEqual(context['event_list'][1], playproduction1)


class MiscEventVisitListViewTestCase(ViewTestCase):

    def test_ancestor(self):
        self.assertTrue(issubclass(views.MiscEventVisitListView,
                                   views.EventListView))

    def test_response_200(self):
        "It should respond with 200."
        response = views.MiscEventVisitListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.MiscEventVisitListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/event_list.html')

    def test_context_event_kind(self):
        response = views.MiscEventVisitListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], 'misc')

    def test_context_events_list(self):
        "It should have the latest MiscEvent events in the context."
        movie = MovieEventFactory(date=make_date('2017-02-10'))
        miscevent1 = MiscEventFactory(date=make_date('2017-02-09'))
        miscevent2 = MiscEventFactory(date=make_date('2017-02-12'))
        response = views.MiscEventVisitListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 2)
        self.assertEqual(context['event_list'][0], miscevent2)
        self.assertEqual(context['event_list'][1], miscevent1)


class ConcertListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.ConcertListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.ConcertListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/concert_list.html')

    def test_context_events_list(self):
        "It should have Concerts in the context, in title_sort order."
        c1 = ConcertFactory(title="Chipmunks")
        c2 = ConcertFactory(title="The Aardvarks")
        c3 = ConcertFactory(title="A Bat")
        response = views.ConcertListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('concert_list', context)
        self.assertEqual(len(context['concert_list']), 3)
        self.assertEqual(context['concert_list'][0], c2)
        self.assertEqual(context['concert_list'][1], c3)
        self.assertEqual(context['concert_list'][2], c1)


class MovieListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.MovieListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.MovieListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/movie_list.html')

    def test_context_events_list(self):
        "It should have Movies in the context, in title_sort order."
        m1 = MovieFactory(title="Chipmunks")
        m2 = MovieFactory(title="The Aardvarks")
        m3 = MovieFactory(title="A Bat")
        response = views.MovieListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('movie_list', context)
        self.assertEqual(len(context['movie_list']), 3)
        self.assertEqual(context['movie_list'][0], m2)
        self.assertEqual(context['movie_list'][1], m3)
        self.assertEqual(context['movie_list'][2], m1)


class PlayListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.PlayListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.PlayListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/play_list.html')

    def test_context_events_list(self):
        "It should have Plays in the context, in title_sort order."
        p1 = PlayFactory(title="Chipmunks")
        p2 = PlayFactory(title="The Aardvarks")
        p3 = PlayFactory(title="A Bat")
        response = views.PlayListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('play_list', context)
        self.assertEqual(len(context['play_list']), 3)
        self.assertEqual(context['play_list'][0], p2)
        self.assertEqual(context['play_list'][1], p3)
        self.assertEqual(context['play_list'][2], p1)


class MiscEventListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.MiscEventListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.MiscEventListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/miscevent_list.html')

    def test_context_events_list(self):
        "It should have MiscEvents in the context, in title_sort order."
        e1 = MiscEventFactory(title="Crazy Event")
        e2 = MiscEventFactory(title="The AAA Event")
        e3 = MiscEventFactory(title="A Bad Event")
        response = views.MiscEventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('miscevent_list', context)
        self.assertEqual(len(context['miscevent_list']), 3)
        self.assertEqual(context['miscevent_list'][0], e2)
        self.assertEqual(context['miscevent_list'][1], e3)
        self.assertEqual(context['miscevent_list'][2], e1)


class VenueListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.VenueListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.VenueListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events/venue_list.html')

    def test_context_events_list(self):
        "It should have Venues in the context, in title_sort order."
        p1 = VenueFactory(name="Classic Venue")
        p2 = VenueFactory(name="The Amazing Venue")
        p3 = VenueFactory(name="A Brilliant Venue")
        response = views.VenueListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('venue_list', context)
        self.assertEqual(len(context['venue_list']), 3)
        self.assertEqual(context['venue_list'][0], p2)
        self.assertEqual(context['venue_list'][1], p3)
        self.assertEqual(context['venue_list'][2], p1)


class ConcertDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.concert = ConcertFactory(pk=3)

    def test_response_200(self):
        "It should respond with 200."
        response = views.ConcertDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Concert with that pk."
        with self.assertRaises(Http404):
            response = views.ConcertDetailView.as_view()(self.request, pk=5)

    def test_templates(self):
        response = views.ConcertDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.template_name[0],
                         'spectator/events/concert_detail.html')

    def test_context(self):
        "It should have the concert in the context."
        response = views.ConcertDetailView.as_view()(self.request, pk=3)
        context = response.context_data
        self.assertIn('concert', context)
        self.assertEqual(context['concert'], self.concert)


class MovieDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.movie = MovieFactory(pk=3)

    def test_response_200(self):
        "It should respond with 200."
        response = views.MovieDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Movie with that pk."
        with self.assertRaises(Http404):
            response = views.MovieDetailView.as_view()(self.request, pk=5)

    def test_templates(self):
        response = views.MovieDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.template_name[0],
                         'spectator/events/movie_detail.html')

    def test_context(self):
        "It should have the movie in the context."
        response = views.MovieDetailView.as_view()(self.request, pk=3)
        context = response.context_data
        self.assertIn('movie', context)
        self.assertEqual(context['movie'], self.movie)


class PlayDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.play = PlayFactory(pk=3)

    def test_response_200(self):
        "It should respond with 200."
        response = views.PlayDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Play with that pk."
        with self.assertRaises(Http404):
            response = views.PlayDetailView.as_view()(self.request, pk=5)

    def test_templates(self):
        response = views.PlayDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.template_name[0],
                         'spectator/events/play_detail.html')

    def test_context(self):
        "It should have the play in the context."
        response = views.PlayDetailView.as_view()(self.request, pk=3)
        context = response.context_data
        self.assertIn('play', context)
        self.assertEqual(context['play'], self.play)


class MiscEventDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.miscevent = MiscEventFactory(pk=3)

    def test_response_200(self):
        "It should respond with 200."
        response = views.MiscEventDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no MiscEvent with that pk."
        with self.assertRaises(Http404):
            response = views.MiscEventDetailView.as_view()(self.request, pk=5)

    def test_templates(self):
        response = views.MiscEventDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.template_name[0],
                         'spectator/events/miscevent_detail.html')

    def test_context(self):
        "It should have the miscevent in the context."
        response = views.MiscEventDetailView.as_view()(self.request, pk=3)
        context = response.context_data
        self.assertIn('miscevent', context)
        self.assertEqual(context['miscevent'], self.miscevent)


class VenueDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.venue = VenueFactory(pk=3)

    def test_ancestor(self):
        self.assertTrue(issubclass(views.VenueListView,
                                   views.PaginatedListView))

    def test_response_200(self):
        "It should respond with 200."
        response = views.VenueDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Venue with that pk."
        with self.assertRaises(Http404):
            response = views.VenueDetailView.as_view()(self.request, pk=5)

    def test_templates(self):
        response = views.VenueDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.template_name[0],
                         'spectator/events/venue_detail.html')

    def test_context_venue(self):
        "It should have the venue in the context."
        response = views.VenueDetailView.as_view()(self.request, pk=3)
        context = response.context_data
        self.assertIn('venue', context)
        self.assertEqual(context['venue'], self.venue)

    def test_context_event_list(self):
        "It should have the venue's events in the context."
        MovieEventFactory.create_batch(3, venue=self.venue)
        MovieEventFactory()
        response = views.VenueDetailView.as_view()(self.request, pk=3)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 3)

    @override_settings(SPECTATOR_GOOGLE_MAPS_API_KEY='123456')
    def test_context_map_on(self):
        "It should put the api key in context when it, and lat/lon, exist."
        venue = VenueFactory(pk=4, latitude=51, longitude=0)
        response = views.VenueDetailView.as_view()(self.request, pk=4)
        self.assertIn('SPECTATOR_GOOGLE_MAPS_API_KEY', response.context_data)
        self.assertEqual(response.context_data['SPECTATOR_GOOGLE_MAPS_API_KEY'],
                        '123456')

    @override_settings(SPECTATOR_GOOGLE_MAPS_API_KEY='123456')
    def test_context_map_off_1(self):
        "It should NOT put the api key in context when it exists but lat/lon, don't."
        venue = VenueFactory(pk=4, latitude=None, longitude=None)
        response = views.VenueDetailView.as_view()(self.request, pk=4)
        self.assertNotIn('SPECTATOR_GOOGLE_MAPS_API_KEY', response.context_data)

    @override_settings()
    def test_context_map_off_2(self):
        "It should NOT put the api key in context when it does not exist but lat/lon do."
        del settings.SPECTATOR_GOOGLE_MAPS_API_KEY
        venue = VenueFactory(pk=4, latitude=51, longitude=0)
        response = views.VenueDetailView.as_view()(self.request, pk=4)
        self.assertNotIn('SPECTATOR_GOOGLE_MAPS_API_KEY', response.context_data)


def EventYearArchiveViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.con1 = ConcertFactory(date=make_date('2017-01-31'))

    def test_response_200(self):
        "It should respond with 200 if there's an event in that year."
        response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if it's a date before our first year."
        with self.assertRaises(Http404):
            response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2016')

    def test_templates(self):
        response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertEqual(response.template_name[0],
                         'spectator/events/events_archive_year.html')

    def test_context_event_list(self):
        "It should only include events in chosen year, earliest first."
        con2 = ConcertFactory(date=make_date('2016-07-15'))
        con3 = ConcertFactory(date=make_date('2017-01-20'))

        response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2017')
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 2)
        self.assertEqual(context['event_list'][0], con3)
        self.assertEqual(context['reading_list'][1], self.con1)

    def test_context_year(self):
        "Context should include a date object representing the chosen year."
        response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertIn('year', response.context_data)
        self.assertEqual(response.context_data['year'], make_date('2017-01-01'))

    def test_context_next_prev_years(self):
        "Context should include date objects representing next/prev years, if any."
        ConcertFactory(date=make_date('2016-07-15'))
        response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertIn('previous_year', response.context_data)
        self.assertIn('next_year', response.context_data)
        self.assertEqual(response.context_data['previous_year'],
                        make_date('2016-01-01'))
        self.assertIsNone(response.context_data['next_year'])

    def test_context_no_prev_year(self):
        "There should be no previous year if we're on the earliest year."
        response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertIn('previous_year', response.context_data)
        self.assertIsNone(response.context_data['previous_year'])

