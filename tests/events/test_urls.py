from django.test import TestCase
from django.urls import resolve, reverse

from .. import make_date
from spectator.events import views
from spectator.events.factories import GigEventFactory


class EventsUrlsTestCase(TestCase):

    # HOME

    def test_events_home_url(self):
        self.assertEqual(reverse("spectator:events:home"), "/events/")

    def test_events_home_view(self):
        "Should use the correct view."
        self.assertEqual(resolve("/events/").func.view_class, views.EventListView)

    # VENUES

    def test_venue_list_url(self):
        self.assertEqual(reverse("spectator:events:venue_list"), "/events/venues/")

    def test_venue_list_view(self):
        "Should use the correct view."
        self.assertEqual(
            resolve("/events/venues/").func.view_class, views.VenueListView
        )

    def test_venue_detail_url(self):
        self.assertEqual(
            reverse("spectator:events:venue_detail", kwargs={"slug": "my-venue"}),
            "/events/venues/my-venue/",
        )

    def test_venue_detail_view(self):
        "Should use the correct view."
        self.assertEqual(
            resolve("/events/venues/my-venue/").func.view_class, views.VenueDetailView
        )

    # YEARS

    def test_event_year_archive_url(self):
        GigEventFactory(date=make_date("2017-02-15"))
        self.assertEqual(
            reverse("spectator:events:event_year_archive", kwargs={"year": 2017}),
            "/events/2017/",
        )

    def test_event_year_archive_view(self):
        "Should use the correct view."
        GigEventFactory(date=("2017-02-15"))
        self.assertEqual(
            resolve("/events/2017/").func.view_class, views.EventYearArchiveView
        )

    # EVENTS

    def test_event_list_url(self):
        self.assertEqual(
            reverse("spectator:events:event_list", kwargs={"kind_slug": "gigs"}),
            "/events/types/gigs/",
        )

    def test_event_list_view(self):
        "Should use the correct view."
        self.assertEqual(
            resolve("/events/types/gigs/").func.view_class, views.EventListView
        )

    def test_event_detail_url(self):
        self.assertEqual(
            reverse("spectator:events:event_detail", kwargs={"slug": "my-event"}),
            "/events/my-event/",
        )

    def test_event_detail_view(self):
        "Should use the correct view."
        self.assertEqual(
            resolve("/events/my-event/").func.view_class, views.EventDetailView
        )

    # WORKS

    def test_work_list_url(self):
        self.assertEqual(
            reverse("spectator:events:work_list", kwargs={"kind_slug": "movies"}),
            "/events/movies/",
        )

    def test_work_list_view(self):
        "Should use the correct view."
        self.assertEqual(resolve("/events/movies/").func.view_class, views.WorkListView)

    def test_work_detail_url(self):
        self.assertEqual(
            reverse(
                "spectator:events:work_detail",
                kwargs={"kind_slug": "movies", "slug": "my-work"},
            ),
            "/events/movies/my-work/",
        )

    def test_work_detail_view(self):
        "Should use the correct view."
        self.assertEqual(
            resolve("/events/movies/my-work/").func.view_class, views.WorkDetailView
        )
