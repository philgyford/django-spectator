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
from spectator.factories import IndividualCreatorFactory,\
        PublicationFactory, PublicationSeriesFactory, ReadingFactory


class ViewsTestCase(TestCase):

    def setUp(self):
        self.factory = RequestFactory()

    def test_home_response_200(self):
        "It should respond with 200."
        request = self.factory.get('/')
        response = views.HomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_creator_list_response_200(self):
        "It should respond with 200."
        request = self.factory.get('/creators/')
        response = views.CreatorListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_creator_detail_response_200(self):
        "It should respond with 200 if there's a Creator with that pk."
        IndividualCreatorFactory(pk=3)
        request = self.factory.get('/creators/3/')
        response = views.CreatorDetailView.as_view()(request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_creator_detail_response_404(self):
        "It should raise 404 if there's no Creator with that pk."
        IndividualCreatorFactory(pk=3)
        request = self.factory.get('/creators/5/')
        with self.assertRaises(Http404):
            response = views.CreatorDetailView.as_view()(request, pk=5)

    def test_reading_home_response_200(self):
        "It should respond with 200."
        request = self.factory.get('/reading/')
        response = views.ReadingHomeView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_publicationseries_list_response_200(self):
        "It should respond with 200."
        request = self.factory.get('/reading/series/')
        response = views.PublicationSeriesListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_publicationseries_detail_response_200(self):
        "It should respond with 200 if there's a PublicationSeries with that pk."
        PublicationSeriesFactory(pk=3)
        request = self.factory.get('/reading/series/3/')
        response = views.PublicationSeriesDetailView.as_view()(request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_publicationseries_detail_response_404(self):
        "It should raise 404 if there's no PublicationSeries with that pk."
        PublicationSeriesFactory(pk=3)
        request = self.factory.get('/reading/series/5/')
        with self.assertRaises(Http404):
            response = views.PublicationSeriesDetailView.as_view()(
                                                                request, pk=5)

    def test_publication_list_response_200(self):
        "It should respond with 200."
        request = self.factory.get('/reading/publications/')
        response = views.PublicationListView.as_view()(request)
        self.assertEqual(response.status_code, 200)

    def test_publication_detail_response_200(self):
        "It should respond with 200 if there's a Publication with that pk."
        PublicationFactory(pk=3)
        request = self.factory.get('/reading/publications/3/')
        response = views.PublicationDetailView.as_view()(request, pk=3)
        self.assertEqual(response.status_code, 200)

    def test_publication_detail_response_404(self):
        "It should raise 404 if there's no Publication with that pk."
        PublicationFactory(pk=3)
        request = self.factory.get('/reading/publications/5/')
        with self.assertRaises(Http404):
            response = views.PublicationDetailView.as_view()(request, pk=5)

    def test_reading_year_archive_response_200(self):
        "It should respond with 200 if there's a Reading ending in that year."
        ReadingFactory(
                end_date=datetime.strptime('2017-02-15', "%Y-%m-%d").date())
        request = self.factory.get('/reading/2017/')
        response = views.ReadingYearArchiveView.as_view()(request, year='2017')
        self.assertEqual(response.status_code, 200)

    def test_reading_year_archive_response_404(self):
        "It should raise 404 if there's no Reading ending in that year."
        ReadingFactory(
                end_date=datetime.strptime('2017-02-15', "%Y-%m-%d").date())
        request = self.factory.get('/reading/2016/')
        with self.assertRaises(Http404):
            response = views.ReadingYearArchiveView.as_view()(
                                                        request, year='2016')

