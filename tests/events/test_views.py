from django.conf import settings
from django.http.response import Http404
from django.test import override_settings

from .. import make_date
from ..core.test_views import ViewTestCase
from spectator.events import views
from spectator.events.factories import *


class EventListViewTestCase(ViewTestCase):

    def test_ancestor(self):
        self.assertTrue(issubclass(views.EventListView,
                                   views.PaginatedListView))

    def test_response_200(self):
        "It should respond with 200."
        response = views.EventListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should respond with 404 with an invalid kind_slug."
        with self.assertRaises(Http404):
            response = views.EventListView.as_view()(
                                            self.request, kind_slug='nope')

    def test_templates(self):
        response = views.EventListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                'spectator_events/event_list.html')

    def test_context_counts(self):
        ConcertEventFactory.create_batch(6)
        DanceEventFactory.create_batch(5)
        GigEventFactory.create_batch(4)
        MiscEventFactory.create_batch(3)
        MovieEventFactory.create_batch(2)
        PlayEventFactory.create_batch(1)
        response = views.EventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('counts', context)
        counts = context['counts']
        self.assertIn('all', counts)
        self.assertEqual(counts['all'], 21)
        self.assertIn('concert', counts)
        self.assertEqual(counts['concert'], 6)
        self.assertIn('dance', counts)
        self.assertEqual(counts['dance'], 5)
        self.assertIn('gig', counts)
        self.assertEqual(counts['gig'], 4)
        self.assertIn('misc', counts)
        self.assertEqual(counts['misc'], 3)
        self.assertIn('movie', counts)
        self.assertEqual(counts['movie'], 2)
        self.assertIn('play', counts)
        self.assertEqual(counts['play'], 1)

    def test_context_event_kind(self):
        response = views.EventListView.as_view()(self.request, kind_slug='gigs')
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], 'gig')

    def test_context_event_kind_none(self):
        "When viewing all events, event_kind should be None"
        response = views.EventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], None)

    def test_context_event_list(self):
        "It should have the latest events, of all kinds, in the context."
        movie = MovieEventFactory(    date=make_date('2017-02-10'))
        play = PlayEventFactory(      date=make_date('2017-02-09'))
        gig = GigEventFactory(        date=make_date('2017-02-12'))
        misc = MiscEventFactory(      date=make_date('2017-02-05'))
        concert = ConcertEventFactory(date=make_date('2017-02-14'))
        dance = DanceEventFactory(    date=make_date('2017-02-03'))
        response = views.EventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 6)
        self.assertEqual(context['event_list'][0], concert)
        self.assertEqual(context['event_list'][1], gig)
        self.assertEqual(context['event_list'][2], movie)
        self.assertEqual(context['event_list'][3], play)
        self.assertEqual(context['event_list'][4], misc)
        self.assertEqual(context['event_list'][5], dance)


class EventDetailViewTestCase(ViewTestCase):
    "A basic EventDetail page e.g. for a gig or misc Event."

    def setUp(self):
        super().setUp()
        self.event = GigEventFactory(pk=3)

    def test_response_200(self):
        "It should respond with 200."
        response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='gigs', pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404_kind_slug(self):
        "It should raise 404 if there's no Event with that kind_slug."
        with self.assertRaises(Http404):
            response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='nope', pk=3)

    def test_response_404_pk(self):
        "It should raise 404 if there's no Event with that pk."
        with self.assertRaises(Http404):
            response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='gigs', pk=5)

    def test_templates(self):
        response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='gigs', pk=3)
        self.assertEqual(response.template_name[0],
                'spectator_events/event_detail.html')

    def test_context(self):
        "It should have the event in the context."
        response = views.EventDetailView.as_view()(self.request, pk=3)
        context = response.context_data
        self.assertIn('event', context)
        self.assertEqual(context['event'], self.event)


class MovieEventDetailViewTestCase(ViewTestCase):
    "Movie Events are a bit different to the standard."

    def setUp(self):
        super().setUp()
        self.event = MovieEventFactory(pk=3, movie=MovieFactory(pk=6))

    def test_response_200(self):
        "It should respond with 200."
        response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='movies', pk=6)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Movie with that pk."
        with self.assertRaises(Http404):
            response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='movies', pk=3)

    def test_templates(self):
        response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='movies', pk=6)
        self.assertEqual(response.template_name[0],
                'spectator_events/movie_detail.html')

    def test_context(self):
        "It should have the Movie (not the Event) in the context."
        response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='movies', pk=6)
        context = response.context_data
        self.assertIn('movie', context)
        self.assertEqual(context['movie'], self.event.movie)


class PlayEventDetailViewTestCase(ViewTestCase):
    "Play Events are a bit different to the standard."

    def setUp(self):
        super().setUp()
        self.event = PlayEventFactory(pk=3, play=PlayFactory(pk=6))

    def test_response_200(self):
        "It should respond with 200."
        response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='plays', pk=6)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Play with that pk."
        with self.assertRaises(Http404):
            response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='plays', pk=3)

    def test_templates(self):
        response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='plays', pk=6)
        self.assertEqual(response.template_name[0],
                'spectator_events/play_detail.html')

    def test_context(self):
        "It should have the Play (not the Event) in the context."
        response = views.EventDetailView.as_view()(
                                        self.request, kind_slug='plays', pk=6)
        context = response.context_data
        self.assertIn('play', context)
        self.assertEqual(context['play'], self.event.play)


class EventYearArchiveViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.gig1 = GigEventFactory(date=make_date('2017-01-31'))

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
                         'spectator_events/event_archive_year.html')

    def test_context_event_list(self):
        "It should only include events in chosen year, earliest first."
        gig2 = GigEventFactory(date=make_date('2016-07-15'))
        gig3 = GigEventFactory(date=make_date('2017-01-20'))

        response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2017')
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 2)
        self.assertEqual(context['event_list'][0], gig3)
        self.assertEqual(context['event_list'][1], self.gig1)

    def test_context_year(self):
        "Context should include a date object representing the chosen year."
        response = views.EventYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertIn('year', response.context_data)
        self.assertEqual(response.context_data['year'], make_date('2017-01-01'))

    def test_context_next_prev_years(self):
        "Context should include date objects representing next/prev years."
        GigEventFactory(date=make_date('2016-07-15'))
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


class ClassicalWorkListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.ClassicalWorkListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.ClassicalWorkListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator_events/m2m_work_list.html')

    def test_context(self):
        response = views.ClassicalWorkListView.as_view()(self.request)
        self.assertIn('page_title', response.context_data)
        self.assertEqual(response.context_data['page_title'],
                         'Classical works')


class ClassicalWorkDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        ClassicalWorkFactory(pk=5)

    def test_response_200(self):
        "It should respond with 200."
        response = views.ClassicalWorkDetailView.as_view()(self.request, pk=5)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should respond with 404."
        with self.assertRaises(Http404):
            response = views.ClassicalWorkDetailView.as_view()(
                                                            self.request, pk=3)

    def test_templates(self):
        response = views.ClassicalWorkDetailView.as_view()(self.request, pk=5)
        self.assertEqual(response.template_name[0],
                         'spectator_events/m2m_work_detail.html')

    def test_context(self):
        response = views.ClassicalWorkDetailView.as_view()(self.request, pk=5)
        self.assertIn('breadcrumb_list_title', response.context_data)
        self.assertEqual(response.context_data['breadcrumb_list_title'],
                         'Classical works')
        self.assertIn('breadcrumb_list_url', response.context_data)
        self.assertEqual(response.context_data['breadcrumb_list_url'],
                         '/events/concerts/works/')


class DancePieceListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.DancePieceListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.DancePieceListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator_events/m2m_work_list.html')

    def test_context(self):
        response = views.DancePieceListView.as_view()(self.request)
        self.assertIn('page_title', response.context_data)
        self.assertEqual(response.context_data['page_title'],
                         'Dance pieces')


class DancePieceDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        DancePieceFactory(pk=5)

    def test_response_200(self):
        "It should respond with 200."
        response = views.DancePieceDetailView.as_view()(self.request, pk=5)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should respond with 404."
        with self.assertRaises(Http404):
            response = views.DancePieceDetailView.as_view()(self.request, pk=3)

    def test_templates(self):
        response = views.DancePieceDetailView.as_view()(self.request, pk=5)
        self.assertEqual(response.template_name[0],
                         'spectator_events/m2m_work_detail.html')

    def test_context(self):
        response = views.DancePieceDetailView.as_view()(self.request, pk=5)
        self.assertIn('breadcrumb_list_title', response.context_data)
        self.assertEqual(response.context_data['breadcrumb_list_title'],
                         'Dance pieces')
        self.assertIn('breadcrumb_list_url', response.context_data)
        self.assertEqual(response.context_data['breadcrumb_list_url'],
                         '/events/dance/pieces/')


class VenueListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.VenueListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.VenueListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                'spectator_events/venue_list.html')

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
                'spectator_events/venue_detail.html')

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

