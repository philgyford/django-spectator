from django.conf import settings
from django.http.response import Http404

from freezegun import freeze_time


from .. import make_date, override_app_settings
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
        CinemaEventFactory.create_batch(2)
        TheatreEventFactory.create_batch(1)
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
        self.assertIn('cinema', counts)
        self.assertEqual(counts['cinema'], 2)
        self.assertIn('theatre', counts)
        self.assertEqual(counts['theatre'], 1)

    def test_context_event_kind(self):
        response = views.EventListView.as_view()(self.request, kind_slug='gigs')
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], 'gig')
        self.assertEqual(context['event_kind_name'], 'Gig')
        self.assertEqual(context['event_kind_name_plural'], 'Gigs')

    def test_context_event_kind_none(self):
        "When viewing all events, event_kind should be None"
        response = views.EventListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_kind', context)
        self.assertEqual(context['event_kind'], None)
        self.assertNotIn('event_kind_name', context)
        self.assertNotIn('event_kind_name_plural', context)

    def test_context_event_list(self):
        "It should have the latest events, of all kinds, in the context."
        movie = CinemaEventFactory(    date=make_date('2017-02-10'))
        play = TheatreEventFactory(      date=make_date('2017-02-09'))
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
        self.event = GigEventFactory(pk=123)

    def test_response_200(self):
        "It should respond with 200."
        response = views.EventDetailView.as_view()(
                                        self.request, slug='9g5o8')
        self.assertEqual(response.status_code, 200)

    def test_response_404_pk(self):
        "It should raise 404 if there's no Event with that slug."
        with self.assertRaises(Http404):
            response = views.EventDetailView.as_view()(
                                        self.request, slug='nope')

    def test_templates(self):
        response = views.EventDetailView.as_view()(
                                        self.request, slug='9g5o8')
        self.assertEqual(response.template_name[0],
                'spectator_events/event_detail.html')

    def test_context(self):
        "It should have the event in the context."
        response = views.EventDetailView.as_view()(
                                self.request, slug='9g5o8')
        context = response.context_data
        self.assertIn('event', context)
        self.assertEqual(context['event'], self.event)


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

    @freeze_time("2017-06-01 12:00:00")
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


class WorkListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.WorkListView.as_view()(self.request, kind_slug='movies')
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.WorkListView.as_view()(self.request, kind_slug='movies')
        self.assertEqual(response.template_name[0],
                         'spectator_events/work_list.html')

    def test_context(self):
        response = views.WorkListView.as_view()(self.request, kind_slug='movies')
        context = response.context_data
        self.assertEqual(context['page_title'], 'Movies')
        self.assertEqual(context['work_kind'], 'movie')
        self.assertEqual(context['work_kind_name'], 'Movie')
        self.assertEqual(context['work_kind_name_plural'], 'Movies')
        self.assertEqual(context['breadcrumb_list_title'], 'Movies')
        self.assertEqual(context['breadcrumb_list_url'], '/events/movies/')


class WorkDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        MovieFactory(pk=123)

    def test_response_200(self):
        "It should respond with 200."
        response = views.WorkDetailView.as_view()(self.request,
                                            kind_slug='movies', slug='9g5o8')
        self.assertEqual(response.status_code, 200)

    def test_response_404_invalid_slug(self):
        "It should respond with 404."
        with self.assertRaises(Http404):
            response = views.WorkDetailView.as_view()(self.request,
                                            kind_slug='movies', slug='nope')

    def test_response_404_invalid_kind_slug(self):
        "It should respond with 404."
        with self.assertRaises(Http404):
            response = views.WorkDetailView.as_view()(self.request,
                                                kind_slug='nope', slug='9g5o8')

    def test_templates(self):
        response = views.WorkDetailView.as_view()(self.request,
                                            kind_slug='movies', slug='9g5o8')
        self.assertEqual(response.template_name[0],
                         'spectator_events/work_detail.html')

    def test_context(self):
        response = views.WorkDetailView.as_view()(self.request,
                                                kind_slug='movies', slug='9g5o8')
        self.assertIn('breadcrumb_list_title', response.context_data)
        self.assertEqual(response.context_data['breadcrumb_list_title'],
                         'Movies')
        self.assertIn('breadcrumb_list_url', response.context_data)
        self.assertEqual(response.context_data['breadcrumb_list_url'],
                         '/events/movies/')


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
        v1 = VenueFactory(name="Classic Venue")
        v2 = VenueFactory(name="The Amazing Venue")
        v3 = VenueFactory(name="A Brilliant Venue")
        response = views.VenueListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('venue_list', context)
        self.assertEqual(len(context['venue_list']), 3)
        self.assertEqual(context['venue_list'][0], v2)
        self.assertEqual(context['venue_list'][1], v3)
        self.assertEqual(context['venue_list'][2], v1)

    def test_context_country_list(self):
        VenueFactory(country='') # Should not be counted.
        VenueFactory(country='UY')
        VenueFactory.create_batch(4, country='CH')
        VenueFactory.create_batch(2, country='GB')
        response = views.VenueListView.as_view()(self.request)
        context = response.context_data
        self.assertIn('country_list', context)
        self.assertEqual(len(context['country_list']), 3)
        self.assertEqual(context['country_list'][0],
                        {'code':'CH', 'name':'Switzerland'})
        self.assertEqual(context['country_list'][1],
                        {'code':'GB', 'name':'UK'})
        self.assertEqual(context['country_list'][2],
                        {'code':'UY', 'name':'Uruguay'})


class VenueDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        self.venue = VenueFactory(pk=123)

    def test_ancestor(self):
        self.assertTrue(issubclass(views.VenueListView,
                                   views.PaginatedListView))

    def test_response_200(self):
        "It should respond with 200."
        response = views.VenueDetailView.as_view()(self.request, slug='9g5o8')
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Venue with that slug."
        with self.assertRaises(Http404):
            response = views.VenueDetailView.as_view()(self.request, slug='nope')

    def test_templates(self):
        response = views.VenueDetailView.as_view()(self.request, slug='9g5o8')
        self.assertEqual(response.template_name[0],
                'spectator_events/venue_detail.html')

    def test_context_venue(self):
        "It should have the venue in the context."
        response = views.VenueDetailView.as_view()(self.request, slug='9g5o8')
        context = response.context_data
        self.assertIn('venue', context)
        self.assertEqual(context['venue'], self.venue)

    def test_context_event_list(self):
        "It should have the venue's events in the context."
        CinemaEventFactory.create_batch(3, venue=self.venue)
        CinemaEventFactory()
        response = views.VenueDetailView.as_view()(self.request, slug='9g5o8')
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 3)

    @override_app_settings(GOOGLE_MAPS_API_KEY='123456')
    def test_context_map_on(self):
        "It should put the api key in context when it, and lat/lon, exist."
        venue = VenueFactory(pk=456, latitude=51, longitude=0)
        response = views.VenueDetailView.as_view()(self.request, slug='8wozp')
        self.assertIn('SPECTATOR_GOOGLE_MAPS_API_KEY', response.context_data)
        self.assertEqual(response.context_data['SPECTATOR_GOOGLE_MAPS_API_KEY'],
                        '123456')

    @override_app_settings(GOOGLE_MAPS_API_KEY='123456')
    def test_context_map_off_1(self):
        "It should NOT put the api key in context when it exists but lat/lon, don't."
        venue = VenueFactory(pk=456, latitude=None, longitude=None)
        response = views.VenueDetailView.as_view()(self.request, slug='8wozp')
        self.assertNotIn('SPECTATOR_GOOGLE_MAPS_API_KEY', response.context_data)

    @override_app_settings(GOOGLE_MAPS_API_KEY='')
    def test_context_map_off_2(self):
        "It should NOT put the api key in context when it does not exist but lat/lon do."
        venue = VenueFactory(pk=456, latitude=51, longitude=0)
        response = views.VenueDetailView.as_view()(self.request, slug='8wozp')
        self.assertNotIn('SPECTATOR_GOOGLE_MAPS_API_KEY', response.context_data)
