from .test_core import ViewTestCase
from .. import make_date
from spectator import views
from spectator.factories import ConcertFactory, MovieEventFactory,\
        PlayProductionEventFactory


class EventsHomeViewTestCase(ViewTestCase):
    def test_response_200(self):
        "It should respond with 200."
        response = views.EventsHomeView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.EventsHomeView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/events_home.html')

    def test_context_events_list(self):
        "It should have the latest events in the context."
        movie = MovieEventFactory(        date=make_date('2017-02-10'))
        play = PlayProductionEventFactory(date=make_date('2017-02-09'))
        concert = ConcertFactory(    date=make_date('2017-02-12'))
        response = views.EventsHomeView.as_view()(self.request)
        context = response.context_data
        self.assertIn('event_list', context)
        self.assertEqual(len(context['event_list']), 3)
        self.assertEqual(context['event_list'][0], concert)
        self.assertEqual(context['event_list'][1], movie)
        self.assertEqual(context['event_list'][2], play)

