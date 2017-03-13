from django.http.response import Http404
from django.test import RequestFactory, TestCase
try:
    # Django >= 1.10
    from django.urls import reverse
except ImportError:
    # Django < 1.10
    from django.core.urlresolvers import reverse

from . import make_date
from spectator import views
from spectator.factories import GroupCreatorFactory, IndividualCreatorFactory,\
        PublicationFactory, PublicationSeriesFactory, ReadingFactory


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
        self.assertEqual(response.template_name[0], 'spectator/home.html')

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
        self.assertIn('in_progress_publications', context)
        self.assertEqual(len(context['in_progress_publications']), 1)
        self.assertEqual(context['in_progress_publications'][0],
                                                    in_progress.publication)


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

    def test_context_in_progress(self):
        "It should have in-progress publications in the context."
        in_progress = ReadingFactory(
                start_date=make_date('2017-02-10'),
            )
        finished = ReadingFactory(
                start_date=make_date('2017-01-15'),
                end_date=make_date('2017-01-28'),
            )
        response = views.ReadingHomeView.as_view()(self.request)
        context = response.context_data
        self.assertIn('in_progress_publications', context)
        self.assertEqual(len(context['in_progress_publications']), 1)
        self.assertEqual(context['in_progress_publications'][0],
                                                    in_progress.publication)


class PublicationSeriesListViewTestCase(ViewTestCase):

    def test_response_200(self):
        "It should respond with 200."
        response = views.PublicationSeriesListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)


class PublicationSeriesDetailViewTestCase(ViewTestCase):

    def setUp(self):
        super().setUp()
        series = PublicationSeriesFactory(pk=3)
        PublicationFactory.create_batch(2, series=series)

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

    def test_context_series(self):
        "It should include the PublicationSeries in the context."
        response = views.PublicationSeriesDetailView.as_view()(
                                                        self.request, pk=3)
        self.assertIn('publicationseries', response.context_data)
        self.assertEqual(response.context_data['publicationseries'].pk, 3)

    def test_context_publication_list(self):
        "It should include the publication_list in the context."
        response = views.PublicationSeriesDetailView.as_view()(
                                                        self.request, pk=3)
        self.assertIn('publication_list', response.context_data)
        self.assertEqual(len(response.context_data['publication_list']), 2)


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

    def test_non_numeric_page(self):
        "PaginatedListView should raise 404 if we ask for a non-numeric page that isn't 'last'."
        request = self.factory.get('/fake-path/?p=asdf')
        with self.assertRaises(Http404):
            response = views.PublicationListView.as_view()(request)

    def test_last_page(self):
        "PaginatedListView should return last page with ?p=last"
        # Two pages' worth:
        PublicationFactory.create_batch(51)
        request = self.factory.get('/fake-path/?p=last')
        response = views.PublicationListView.as_view()(request)
        # Has the final one publication on the second page:
        self.assertEqual(len(response.context_data['publication_list']), 1)

    def test_invalid_page(self):
        "PaginatedListView should raise 404 if we ask for a page number that doesn't exist."
        # Use a URL with p=99:
        request = self.factory.get('/fake-path/?p=99')
        with self.assertRaises(Http404):
            response = views.PublicationListView.as_view()(request)



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
                publication=PublicationFactory(title='2017 Pub 1'),
                start_date=make_date('2016-12-15'),
                end_date=make_date('2017-01-31'))

    def test_response_200(self):
        "It should respond with 200 if there's a Reading ending in that year."
        response = views.ReadingYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertEqual(response.status_code, 200)

    # def test_response_404(self):
        # "It should raise 404 if there's no Reading ending in that year."
        # with self.assertRaises(Http404):
            # response = views.ReadingYearArchiveView.as_view()(
                                                    # self.request, year='2016')

    def test_context_reading_list(self):
        "Should include Readings ending in chosen year, earliest end_date first."
        ReadingFactory(
                publication=PublicationFactory(title='Old Pub'),
                start_date=make_date('2016-06-15'),
                end_date=make_date('2016-07-15'))
        ReadingFactory(
                publication=PublicationFactory(title='2017 Pub 2'),
                start_date=make_date('2017-01-01'),
                end_date=make_date('2017-01-20'))

        response = views.ReadingYearArchiveView.as_view()(
                                                    self.request, year='2017')
        context = response.context_data
        self.assertIn('reading_list', context)
        self.assertEqual(len(context['reading_list']), 2)
        self.assertEqual(context['reading_list'][0].publication.title,
                        '2017 Pub 2')
        self.assertEqual(context['reading_list'][1].publication.title,
                        '2017 Pub 1')

    def test_context_year(self):
        "Context should include a date object representing the chosen year."
        response = views.ReadingYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertIn('year', response.context_data)
        self.assertEqual(response.context_data['year'], make_date('2017-01-01'))

    def test_context_next_prev_years(self):
        "Context should include date objects representing next/prev years, if any."
        ReadingFactory(
                publication=PublicationFactory(title='Old Pub'),
                start_date=make_date('2016-06-15'),
                end_date=make_date('2016-07-15'))
        response = views.ReadingYearArchiveView.as_view()(
                                                    self.request, year='2017')
        self.assertIn('previous_year', response.context_data)
        self.assertIn('next_year', response.context_data)
        self.assertEqual(response.context_data['previous_year'],
                        make_date('2016-01-01'))
        self.assertIsNone(response.context_data['next_year'])


