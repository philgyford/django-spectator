from django.http.response import Http404
from django.test import RequestFactory, TestCase

from .. import make_date
from spectator.core import views
from spectator.core.factories import GroupCreatorFactory,\
        IndividualCreatorFactory
from spectator.events.factories import GigEventFactory, MovieEventFactory
from spectator.reading.factories import ReadingFactory


class ViewTestCase(TestCase):
    """
    Parent class to use with all the other view test cases.
    """

    def setUp(self):
        self.factory = RequestFactory()
        # We use '/fake-path/' for all tests because not testing URLs here,
        # and the views don't care what the URL is.
        self.request = self.factory.get('/fake-path/')


class HomeViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.HomeView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.HomeView.as_view()(self.request)
        self.assertEqual(response.template_name[0], 'spectator_core/home.html')

    def test_context_in_progress(self):
        "It should have in-progress publications in the context."
        in_progress = ReadingFactory(
                start_date=make_date('2017-02-10'),
            )
        finished = ReadingFactory(
                start_date=make_date('2017-01-15'),
                end_date=make_date('2017-01-28'),
            )
        response = views.HomeView.as_view()(self.request)
        context = response.context_data
        self.assertIn('in_progress_publication_list', context)
        self.assertEqual(len(context['in_progress_publication_list']), 1)
        self.assertEqual(context['in_progress_publication_list'][0],
                                                    in_progress.publication)

    def test_context_recent_events(self):
        "It should have recent Events in the context."
        g1 = GigEventFactory(  date=make_date('2017-02-20'))
        g2 = GigEventFactory(  date=make_date('2017-02-05'))
        m1 = MovieEventFactory(date=make_date('2017-02-10'))
        response = views.HomeView.as_view()(self.request)
        context = response.context_data
        self.assertIn('recent_event_list', context)
        self.assertEqual(len(context['recent_event_list']), 3)
        self.assertEqual(context['recent_event_list'][0], g1)
        self.assertEqual(context['recent_event_list'][1], m1)
        self.assertEqual(context['recent_event_list'][2], g2)


class CreatorListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.CreatorListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.CreatorListView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                'spectator_core/creator_list.html')

    def test_context_individual(self):
        "It should have creator_kind='individual' in the context."
        response = views.CreatorListView.as_view()(self.request)
        self.assertIn('creator_kind', response.context_data)
        self.assertEqual(response.context_data['creator_kind'], 'individual')

    def test_context_group(self):
        "It should have creator_kind='group' in the context."
        response = views.CreatorListView.as_view()(self.request, kind='group')
        self.assertIn('creator_kind', response.context_data)
        self.assertEqual(response.context_data['creator_kind'], 'group')

    def test_context_counts(self):
        "It should include the individual and group counts."
        IndividualCreatorFactory.create_batch(2)
        GroupCreatorFactory.create_batch(3)
        response = views.CreatorListView.as_view()(self.request)
        self.assertIn('individual_count', response.context_data)
        self.assertEqual(response.context_data['individual_count'], 2)
        self.assertIn('group_count', response.context_data)
        self.assertEqual(response.context_data['group_count'], 3)

    def test_queryset_individual(self):
        "It should only include individuals in the creator_list"
        group = GroupCreatorFactory()
        indiv = IndividualCreatorFactory()
        response = views.CreatorListView.as_view()(self.request)
        self.assertEqual(len(response.context_data['creator_list']), 1)
        self.assertEqual(response.context_data['creator_list'][0], indiv)

    def test_queryset_group(self):
        "It should only include groups in the creator_list"
        group = GroupCreatorFactory()
        indiv = IndividualCreatorFactory()
        response = views.CreatorListView.as_view()(self.request, kind='group')
        self.assertEqual(len(response.context_data['creator_list']), 1)
        self.assertEqual(response.context_data['creator_list'][0], group)


class CreatorDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        IndividualCreatorFactory(pk=3)

    def test_response_200(self):
        "It should respond with 200 if there's a Creator with that pk."
        response = views.CreatorDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Creator with that pk."
        with self.assertRaises(Http404):
            response = views.CreatorDetailView.as_view()(self.request, pk=5)

    def test_templates(self):
        response = views.CreatorDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.template_name[0],
                'spectator_core/creator_detail.html')

