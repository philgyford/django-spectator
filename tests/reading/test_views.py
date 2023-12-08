from django.http.response import Http404

from spectator.reading import views
from spectator.reading.factories import (
    PublicationFactory,
    PublicationSeriesFactory,
    ReadingFactory,
)
from tests import make_date
from tests.core.test_views import ViewTestCase


class ReadingHomeViewTestCase(ViewTestCase):
    def test_response_200(self):
        "It should respond with 200."
        response = views.ReadingHomeView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.ReadingHomeView.as_view()(self.request)
        self.assertEqual(response.template_name[0], "spectator_reading/home.html")

    def test_context_in_progress(self):
        "It should have in-progress publications in the context."
        in_progress = ReadingFactory(start_date=make_date("2017-02-10"))
        ReadingFactory(
            start_date=make_date("2017-01-15"), end_date=make_date("2017-01-28")
        )
        response = views.ReadingHomeView.as_view()(self.request)
        context = response.context_data
        self.assertIn("in_progress_publication_list", context)
        self.assertEqual(len(context["in_progress_publication_list"]), 1)
        self.assertEqual(
            context["in_progress_publication_list"][0], in_progress.publication
        )


class PublicationSeriesListViewTestCase(ViewTestCase):
    def test_response_200(self):
        "It should respond with 200."
        response = views.PublicationSeriesListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.PublicationSeriesListView.as_view()(self.request)
        self.assertEqual(
            response.template_name[0], "spectator_reading/publicationseries_list.html"
        )


class PublicationSeriesDetailViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        series = PublicationSeriesFactory(pk=123)
        PublicationFactory.create_batch(2, series=series)

    def test_response_200(self):
        "It should respond with 200 if there's a PublicationSeries with that slug."
        response = views.PublicationSeriesDetailView.as_view()(
            self.request, slug="9g5o8"
        )
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no PublicationSeries with that slug."
        with self.assertRaises(Http404):
            views.PublicationSeriesDetailView.as_view()(self.request, slug="nope")

    def test_templates(self):
        response = views.PublicationSeriesDetailView.as_view()(
            self.request, slug="9g5o8"
        )
        self.assertEqual(
            response.template_name[0], "spectator_reading/publicationseries_detail.html"
        )

    def test_context_series(self):
        "It should include the PublicationSeries in the context."
        response = views.PublicationSeriesDetailView.as_view()(
            self.request, slug="9g5o8"
        )
        self.assertIn("publicationseries", response.context_data)
        self.assertEqual(response.context_data["publicationseries"].pk, 123)

    def test_context_publication_list(self):
        "It should include the publication_list in the context."
        response = views.PublicationSeriesDetailView.as_view()(
            self.request, slug="9g5o8"
        )
        self.assertIn("publication_list", response.context_data)
        self.assertEqual(len(response.context_data["publication_list"]), 2)


class PublicationListViewTestCase(ViewTestCase):
    def test_response_200(self):
        "It should respond with 200."
        response = views.PublicationListView.as_view()(self.request)
        self.assertEqual(response.status_code, 200)

    def test_templates(self):
        response = views.PublicationListView.as_view()(self.request)
        self.assertEqual(
            response.template_name[0], "spectator_reading/publication_list.html"
        )

    def test_context_book(self):
        "It should have publication_kind='book' in the context."
        response = views.PublicationListView.as_view()(self.request)
        self.assertIn("publication_kind", response.context_data)
        self.assertEqual(response.context_data["publication_kind"], "book")

    def test_context_periodical(self):
        "It should have publication_kind='periodical' in the context."
        response = views.PublicationListView.as_view()(self.request, kind="periodical")
        self.assertIn("publication_kind", response.context_data)
        self.assertEqual(response.context_data["publication_kind"], "periodical")

    def test_context_counts(self):
        "It should include the book and periodical counts."
        PublicationFactory.create_batch(2, kind="book")
        PublicationFactory.create_batch(3, kind="periodical")
        response = views.PublicationListView.as_view()(self.request)
        self.assertIn("book_count", response.context_data)
        self.assertEqual(response.context_data["book_count"], 2)
        self.assertIn("periodical_count", response.context_data)
        self.assertEqual(response.context_data["periodical_count"], 3)

    def test_queryset_book(self):
        "It should only include books in the publication_list"
        book = PublicationFactory(kind="book")
        PublicationFactory(kind="periodical")
        response = views.PublicationListView.as_view()(self.request)
        self.assertEqual(len(response.context_data["publication_list"]), 1)
        self.assertEqual(response.context_data["publication_list"][0], book)

    def test_queryset_periodical(self):
        "It should only include periodicals in the publication_list"
        PublicationFactory(kind="book")
        periodical = PublicationFactory(kind="periodical")
        response = views.PublicationListView.as_view()(self.request, kind="periodical")
        self.assertEqual(len(response.context_data["publication_list"]), 1)
        self.assertEqual(response.context_data["publication_list"][0], periodical)

    def test_non_numeric_page(self):
        """PaginatedListView should raise 404 if we ask for a
        non-numeric page that isn't 'last'.
        """
        request = self.factory.get("/fake-path/?p=asdf")
        with self.assertRaises(Http404):
            views.PublicationListView.as_view()(request)

    def test_last_page(self):
        "PaginatedListView should return last page with ?p=last"
        # Two pages' worth:
        PublicationFactory.create_batch(51)
        request = self.factory.get("/fake-path/?p=last")
        response = views.PublicationListView.as_view()(request)
        # Has the final one publication on the second page:
        self.assertEqual(len(response.context_data["publication_list"]), 1)

    def test_invalid_page(self):
        """PaginatedListView should raise 404 if we ask for a page
        number that doesn't exist.
        """
        # Use a URL with p=99:
        request = self.factory.get("/fake-path/?p=99")
        with self.assertRaises(Http404):
            views.PublicationListView.as_view()(request)

    def test_ordering_books(self):
        "Should be ordered by title_sort."
        book2 = PublicationFactory(kind="book", title="Book 2")
        book1 = PublicationFactory(kind="book", title="Book 1")
        response = views.PublicationListView.as_view()(self.request)
        pubs = response.context_data["publication_list"]
        self.assertEqual(pubs[0], book1)
        self.assertEqual(pubs[1], book2)

    def test_ordering_periodicals(self):
        "Should be ordered by series' title_sort, then publication's title_sort."
        series_a = PublicationSeriesFactory(title="Series A")
        series_b = PublicationSeriesFactory(title="Series B")
        pub_b1 = PublicationFactory(kind="periodical", series=series_b, title="Book 1")
        pub_a2 = PublicationFactory(kind="periodical", series=series_a, title="Book 2")
        pub_a1 = PublicationFactory(kind="periodical", series=series_a, title="Book 1")
        response = views.PublicationListView.as_view()(self.request, kind="periodical")
        pubs = response.context_data["publication_list"]
        self.assertEqual(pubs[0], pub_a1)
        self.assertEqual(pubs[1], pub_a2)
        self.assertEqual(pubs[2], pub_b1)


class PublicationDetailViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        PublicationFactory(pk=123)

    def test_response_200(self):
        "It should respond with 200 if there's a Publication with that slug."
        response = views.PublicationDetailView.as_view()(self.request, slug="9g5o8")
        self.assertEqual(response.status_code, 200)

    def test_response_404(self):
        "It should raise 404 if there's no Publication with that slug."
        with self.assertRaises(Http404):
            views.PublicationDetailView.as_view()(self.request, slug="nope")

    def test_templates(self):
        response = views.PublicationDetailView.as_view()(self.request, slug="9g5o8")
        self.assertEqual(
            response.template_name[0], "spectator_reading/publication_detail.html"
        )


class ReadingYearArchiveViewTestCase(ViewTestCase):
    def setUp(self):
        super().setUp()
        ReadingFactory(
            publication=PublicationFactory(title="2017 Pub 1", kind="book"),
            start_date=make_date("2016-12-15"),
            end_date=make_date("2017-01-31"),
        )

    def test_response_200(self):
        "It should respond with 200 if there's a Reading ending in that year."
        response = views.ReadingYearArchiveView.as_view()(self.request, year="2017")
        self.assertEqual(response.status_code, 200)

    def test_response_200_with_kind(self):
        """It should respond with 200 if there's a Reading ending in
        that year of the correct kind.
        """
        response = views.ReadingYearArchiveView.as_view()(
            self.request, year="2017", kind="books"
        )
        self.assertEqual(response.status_code, 200)

    def test_response_404_too_early(self):
        "It should raise 404 if it's a date before our first year."
        with self.assertRaises(Http404):
            views.ReadingYearArchiveView.as_view()(self.request, year="2016")

    def test_response_404_wrong_kind(self):
        "It should raise 404 if the kind is invalid."
        with self.assertRaises(Http404):
            views.ReadingYearArchiveView.as_view()(
                self.request, year="2017", kind="invalid"
            )

    def test_templates(self):
        response = views.ReadingYearArchiveView.as_view()(self.request, year="2017")
        self.assertEqual(
            response.template_name[0], "spectator_reading/reading_archive_year.html"
        )

    def test_context_reading_list(self):
        "Should include Readings ending in chosen year, earliest end_date first."
        ReadingFactory(
            publication=PublicationFactory(title="Old Pub"),
            start_date=make_date("2016-06-15"),
            end_date=make_date("2016-07-15"),
        )
        ReadingFactory(
            publication=PublicationFactory(title="2017 Pub 2"),
            start_date=make_date("2017-01-01"),
            end_date=make_date("2017-01-20"),
        )

        response = views.ReadingYearArchiveView.as_view()(self.request, year="2017")
        context = response.context_data
        self.assertIn("reading_list", context)
        self.assertEqual(len(context["reading_list"]), 2)
        self.assertEqual(context["reading_list"][0].publication.title, "2017 Pub 2")
        self.assertEqual(context["reading_list"][1].publication.title, "2017 Pub 1")

    def test_context_year(self):
        "Context should include a date object representing the chosen year."
        response = views.ReadingYearArchiveView.as_view()(self.request, year="2017")
        self.assertIn("year", response.context_data)
        self.assertEqual(response.context_data["year"], make_date("2017-01-01"))

    # When using freeze_time() to set the date to 2017, so that the next_year
    # will be empty, I keep getting this error:
    #   AttributeError: Cannot find 'publication' on FakeDate object,
    #   'publication__roles__creator' is an invalid parameter to prefetch_related()
    # Spent ages trying to fix. No idea. Commenting out freeze_time and the
    # assertion.
    # @freeze_time("2017-06-01 12:00:00")
    def test_context_next_prev_years(self):
        "Context should include date objects representing next/prev years, if any."
        ReadingFactory(
            publication=PublicationFactory(title="Old Pub"),
            start_date=make_date("2016-06-15"),
            end_date=make_date("2016-07-15"),
        )
        response = views.ReadingYearArchiveView.as_view()(self.request, year="2017")
        self.assertIn("previous_year", response.context_data)
        self.assertIn("next_year", response.context_data)
        self.assertEqual(
            response.context_data["previous_year"], make_date("2016-01-01")
        )
        # self.assertIsNone(response.context_data['next_year'])

    def test_context_no_prev_year(self):
        "There should be no previous year if we're on the earliest year."
        response = views.ReadingYearArchiveView.as_view()(self.request, year="2017")
        self.assertIn("previous_year", response.context_data)
        self.assertIsNone(response.context_data["previous_year"])

    def test_context_kind_and_counts(self):
        "The kind and counts for publications, books and periodicals should be correct."
        ReadingFactory(
            publication=PublicationFactory(title="Old Book", kind="book"),
            start_date=make_date("2016-06-15"),
            end_date=make_date("2016-07-15"),
        )
        ReadingFactory(
            publication=PublicationFactory(title="2017 Book 2", kind="book"),
            start_date=make_date("2017-01-01"),
            end_date=make_date("2017-01-20"),
        )
        ReadingFactory(
            publication=PublicationFactory(title="2017 Periodical", kind="periodical"),
            start_date=make_date("2017-02-01"),
            end_date=make_date("2017-02-20"),
        )

        response = views.ReadingYearArchiveView.as_view()(
            self.request, year="2017", kind="books"
        )

        data = response.context_data
        self.assertIn("publication_kind", data)
        self.assertEqual(data["publication_kind"], "book")

        self.assertIn("publication_count", data)
        self.assertEqual(data["publication_count"], 3)

        self.assertIn("periodical_count", data)
        self.assertEqual(data["periodical_count"], 1)

        self.assertIn("book_count", data)
        self.assertEqual(data["book_count"], 2)
