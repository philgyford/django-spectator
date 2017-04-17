from django.test import TestCase
try:
    # Django >= 1.10
    from django.urls import resolve, reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import resolve, reverse

from spectator.reading import views
from spectator.reading.factories import PublicationFactory,\
        PublicationSeriesFactory, ReadingFactory


class ReadingUrlsTestCase(TestCase):

    def test_reading_home_url(self):
        self.assertEqual(reverse('spectator:reading:home'), '/reading/')

    def test_reading_home_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/reading/').func.__name__,
                         views.ReadingHomeView.__name__)


    def test_publicationseries_list_home_url(self):
        self.assertEqual(reverse('spectator:reading:publicationseries_list'),
                         '/reading/series/')

    def test_publicationseries_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/reading/series/').func.__name__,
                         views.PublicationSeriesListView.__name__)


    def test_publicationseries_detail_url(self):
        PublicationSeriesFactory(pk=3)
        self.assertEqual(
                reverse('spectator:reading:publicationseries_detail', kwargs={'pk': 3}),
                        '/reading/series/3/')

    def test_publicationseries_detail_view(self):
        "Should use the correct view."
        PublicationSeriesFactory(pk=3)
        self.assertEqual(resolve('/reading/series/3/').func.__name__,
                         views.PublicationSeriesDetailView.__name__)


    def test_publication_list_url(self):
        self.assertEqual(reverse('spectator:reading:publication_list'),
                         '/reading/publications/')

    def test_publication_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve('/reading/publications/').func.__name__,
                         views.PublicationListView.__name__)

    def test_publication_list_periodical_url(self):
        self.assertEqual(reverse('spectator:reading:publication_list_periodical'),
                         '/reading/publications/periodicals/')

    def test_publication_list_periodical_view(self):
        "Should use the correct view."
        self.assertEqual(
                resolve('/reading/publications/periodicals/').func.__name__,
                views.PublicationListView.__name__)


    def test_publication_detail_url(self):
        PublicationFactory(pk=3)
        self.assertEqual(
                reverse('spectator:reading:publication_detail', kwargs={'pk': 3}),
                        '/reading/publications/3/')

    def test_publication_detail_view(self):
        "Should use the correct view."
        PublicationFactory(pk=3)
        self.assertEqual(resolve('/reading/publications/3/').func.__name__,
                         views.PublicationDetailView.__name__)


    def test_reading_year_archive_url(self):
        ReadingFactory(end_date=('2017-02-15'))
        self.assertEqual(
                reverse('spectator:reading:reading_year_archive', kwargs={'year': 2017}),
                    '/reading/2017/')

    def test_reading_year_archive_view(self):
        "Should use the correct view."
        ReadingFactory(end_date=('2017-02-15'))
        self.assertEqual(resolve('/reading/2017/').func.__name__,
                         views.ReadingYearArchiveView.__name__)
