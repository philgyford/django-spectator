from django.http.response import Http404

from .test_core import ViewTestCase
from .. import make_date
from spectator import views
from spectator.factories import ConcertFactory, MovieFactory,\
        MovieEventFactory, PlayFactory, PlayProductionEventFactory


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
                         'spectator/event_list.html')

    def test_context_events_list(self):
        "It should have the latest events, of all kinds, in the context."
        movie = MovieEventFactory(        date=make_date('2017-02-10'))
        play = PlayProductionEventFactory(date=make_date('2017-02-09'))
        concert = ConcertFactory(         date=make_date('2017-02-12'))
        response = views.EventsHomeView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 3)
        self.assertEqual(context['event_list'][0], concert)
        self.assertEqual(context['event_list'][1], movie)
        self.assertEqual(context['event_list'][2], play)


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
                         'spectator/event_list.html')

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
                         'spectator/event_list.html')

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
                         'spectator/event_list.html')

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


class ConcertListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.ConcertListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.ConcertListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/concert_list.html')

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
                         'spectator/movie_list.html')

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
                         'spectator/play_list.html')

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


class ConcertDetailViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.ConcertListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.ConcertListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/concert_list.html')

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
                         'spectator/movie_list.html')

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
                         'spectator/concert_detail.html')

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
                         'spectator/movie_detail.html')

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
                         'spectator/play_detail.html')

    def test_context(self):
        "It should have the play in the context."
        response = views.PlayDetailView.as_view()(self.request, pk=3)
        context = response.context_data
        self.assertIn('play', context)
        self.assertEqual(context['play'], self.play)

