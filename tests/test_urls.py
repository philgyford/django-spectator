from datetime import datetime

from django.test import TestCase
try:
    # Django >= 1.10
    from django.urls import resolve, reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import resolve, reverse

from spectator import views
from spectator.factories import IndividualCreatorFactory,\
        PublicationFactory, PublicationSeriesFactory, ReadingFactory


class UrlsTestCase(TestCase):

    def test_home_url(self):
        self.assertEqual(reverse('spectator:home'), '/')

    def test_home_200(self):
        response = self.client.get(reverse('spectator:home'))
        self.assertEquals(response.status_code, 200)

    def test_home_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/').func.__name__,
                         views.HomeView.__name__)


    def test_creator_list_url(self):
        self.assertEqual(reverse('spectator:creator_list'), '/creators/')

    def test_creator_list_200(self):
        response = self.client.get(reverse('spectator:creator_list'))
        self.assertEquals(response.status_code, 200)

    def test_creator_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/creators/').func.__name__,
                         views.CreatorListView.__name__)


    def test_creator_detail_url(self):
        IndividualCreatorFactory(pk=3)
        self.assertEqual(reverse('spectator:creator_detail', kwargs={'pk': 3}),
                        '/creators/3/')

    def test_creator_detail_200(self):
        IndividualCreatorFactory(pk=3)
        response = self.client.get(
                        reverse('spectator:creator_detail', kwargs={'pk': 3}))
        self.assertEquals(response.status_code, 200)

    def test_creator_detail_404(self):
        "Should 404 with a non-existent Creator pk."
        IndividualCreatorFactory(pk=3)
        response = self.client.get(
                        reverse('spectator:creator_detail', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)

    def test_creator_detail_view(self):
        "Should use the correct view."
        IndividualCreatorFactory(pk=3)
        self.assertEqual(resolve('/creators/3/').func.__name__,
                         views.CreatorDetailView.__name__)


    def test_reading_home_url(self):
        self.assertEqual(reverse('spectator:reading_home'), '/reading/')

    def test_reading_home_200(self):
        response = self.client.get(reverse('spectator:reading_home'))
        self.assertEquals(response.status_code, 200)

    def test_reading_home_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/reading/').func.__name__,
                         views.ReadingHomeView.__name__)


    def test_publicationseries_list_home_url(self):
        self.assertEqual(reverse('spectator:publicationseries_list'),
                         '/reading/series/')

    def test_publicationseries_list_200(self):
        response = self.client.get(reverse('spectator:publicationseries_list'))
        self.assertEquals(response.status_code, 200)

    def test_publicationseries_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/reading/series/').func.__name__,
                         views.PublicationSeriesListView.__name__)


    def test_publicationseries_detail_url(self):
        PublicationSeriesFactory(pk=3)
        self.assertEqual(
            reverse('spectator:publicationseries_detail', kwargs={'pk': 3}),
                        '/reading/series/3/')

    def test_publicationseries_detail_200(self):
        PublicationSeriesFactory(pk=3)
        response = self.client.get(
            reverse('spectator:publicationseries_detail', kwargs={'pk': 3}))
        self.assertEquals(response.status_code, 200)

    def test_publicationseries_detail_404(self):
        "Should 404 with a non-existent Creator pk."
        PublicationSeriesFactory(pk=3)
        response = self.client.get(
            reverse('spectator:publicationseries_detail', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)

    def test_publicationseries_detail_view(self):
        "Should use the correct view."
        PublicationSeriesFactory(pk=3)
        self.assertEqual(resolve('/reading/series/3/').func.__name__,
                         views.PublicationSeriesDetailView.__name__)


    def test_publication_list_home_url(self):
        self.assertEqual(reverse('spectator:publication_list'),
                         '/reading/publications/')

    def test_publication_list_200(self):
        response = self.client.get(reverse('spectator:publication_list'))
        self.assertEquals(response.status_code, 200)

    def test_publication_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/reading/publications/').func.__name__,
                         views.PublicationListView.__name__)


    def test_publication_detail_url(self):
        PublicationFactory(pk=3)
        self.assertEqual(
            reverse('spectator:publication_detail', kwargs={'pk': 3}),
                        '/reading/publications/3/')

    def test_publication_detail_200(self):
        PublicationFactory(pk=3)
        response = self.client.get(
            reverse('spectator:publication_detail', kwargs={'pk': 3}))
        self.assertEquals(response.status_code, 200)

    def test_publication_detail_404(self):
        "Should 404 with a non-existent Creator pk."
        PublicationFactory(pk=3)
        response = self.client.get(
            reverse('spectator:publication_detail', kwargs={'pk': 5}))
        self.assertEquals(response.status_code, 404)

    def test_publication_detail_view(self):
        "Should use the correct view."
        PublicationFactory(pk=3)
        self.assertEqual(resolve('/reading/publications/3/').func.__name__,
                         views.PublicationDetailView.__name__)


    def test_reading_year_archive_url(self):
        ReadingFactory(
                end_date=datetime.strptime('2017-02-15', "%Y-%m-%d").date())
        self.assertEqual(
            reverse('spectator:reading_year_archive', kwargs={'year': 2017}),
                    '/reading/2017/')

    def test_reading_year_archive_200(self):
        ReadingFactory(
                end_date=datetime.strptime('2017-02-15', "%Y-%m-%d").date())
        response = self.client.get(
            reverse('spectator:reading_year_archive', kwargs={'year': 2017}))
        self.assertEquals(response.status_code, 200)

    def test_reading_year_archive_404(self):
        "It should 404 if there are no Readings for that year."
        ReadingFactory(
                end_date=datetime.strptime('2017-02-15', "%Y-%m-%d").date())
        response = self.client.get(
            reverse('spectator:reading_year_archive', kwargs={'year': 2016}))
        self.assertEquals(response.status_code, 404)

    def test_reading_year_archive_view(self):
        "Should use the correct view."
        ReadingFactory(
                end_date=datetime.strptime('2017-02-15', "%Y-%m-%d").date())
        self.assertEqual(resolve('/reading/2017/').func.__name__,
                         views.ReadingYearArchiveView.__name__)
