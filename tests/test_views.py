from datetime import datetime

from django.http.response import Http404
from django.test import RequestFactory, TestCase
try:
    # Django >= 1.10
    from django.urls import reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import reverse

from spectator import views
from spectator.factories import GroupCreatorFactory, IndividualCreatorFactory,\
        PublicationFactory, PublicationSeriesFactory, ReadingFactory


class ViewTestCase(TestCase):

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
        self.assertEqual(response.template_name[0], 'spectator/home.html')


class CreatorListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.CreatorListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

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


class ReadingHomeViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.ReadingHomeView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.ReadingHomeView.as_view()(self.request)
        self.assertEqual(response.template_name[0],
                         'spectator/reading_home.html')


class PublicationSeriesListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.PublicationSeriesListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)


class PublicationSeriesDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        PublicationSeriesFactory(pk=3)

    def test_response_200(self):
        "It should respond with 200 if there's a PublicationSeries with that pk."
        response = views.PublicationSeriesDetailView.as_view()(
                                                        self.request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no PublicationSeries with that pk."
        with self.assertRaises(Http404):
            response = views.PublicationSeriesDetailView.as_view()(
                                                        self.request, pk=5)


class PublicationListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.PublicationListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_context_individual(self):
        "It should have publication_kind='book' in the context."
        response = views.PublicationListView.as_view()(self.request)
        self.assertIn('publication_kind', response.context_data)
        self.assertEqual(response.context_data['publication_kind'], 'book')

    def test_context_group(self):
        "It should have publication_kind='periodical' in the context."
        response = views.PublicationListView.as_view()(
                                            self.request, kind='periodical')
        self.assertIn('publication_kind', response.context_data)
        self.assertEqual(response.context_data['publication_kind'],
                                                                'periodical')

    def test_queryset_individual(self):
        "It should only include books in the publication_list"
        book = PublicationFactory(kind='book')
        periodical = PublicationFactory(kind='periodical')
        response = views.PublicationListView.as_view()(self.request)
        self.assertEqual(len(response.context_data['publication_list']), 1)
        self.assertEqual(response.context_data['publication_list'][0], book)

    def test_queryset_group(self):
        "It should only include periodicals in the publication_list"
        book = PublicationFactory(kind='book')
        periodical = PublicationFactory(kind='periodical')
        response = views.PublicationListView.as_view()(
                                            self.request, kind='periodical')
        self.assertEqual(len(response.context_data['publication_list']), 1)
        self.assertEqual(response.context_data['publication_list'][0],
                                                                    periodical)


class PublicationDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        PublicationFactory(pk=3)

    def test_response_200(self):
        "It should respond with 200 if there's a Publication with that pk."
        response = views.PublicationDetailView.as_view()(self.request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Publication with that pk."
        with self.assertRaises(Http404):
            response = views.PublicationDetailView.as_view()(self.request, pk=5)


class ReadingYearArchiveViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        ReadingFactory(
                start_date=datetime.strptime('2016-12-15', "%Y-%m-%d").date(),
                end_date=datetime.strptime('2017-01-15', "%Y-%m-%d").date())

    def test_response_200(self):
        "It should respond with 200 if there's a Reading ending in that year."
        response = views.ReadingYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Reading ending in that year."
        with self.assertRaises(Http404):
            response = views.ReadingYearArchiveView.as_view()(
                                                    self.request, year='2016')

