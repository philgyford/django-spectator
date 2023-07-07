from django.urls import path, re_path

from . import views
from .models import Event, Work

app_name = "events"

# Will be like 'movies|plays|concerts' etc:
event_kind_slugs = "|".join(Event.get_valid_kind_slugs())

# Will be like 'classical-works|dance-pieces' etc:
work_kind_slugs = "|".join(Work.get_valid_kind_slugs())

urlpatterns = [
    path("", view=views.EventListView.as_view(), name="home"),
    re_path(
        rf"^types/(?P<kind_slug>{event_kind_slugs})/$",
        view=views.EventListView.as_view(),
        name="event_list",
    ),
    path(
        "venues/",
        view=views.VenueListView.as_view(),
        name="venue_list",
    ),
    re_path(
        r"^venues/(?P<slug>[\w-]+)/$",
        view=views.VenueDetailView.as_view(),
        name="venue_detail",
    ),
    re_path(
        r"^(?P<year>[0-9]{4})/$",
        view=views.EventYearArchiveView.as_view(),
        name="event_year_archive",
    ),
    re_path(
        rf"^(?P<kind_slug>{work_kind_slugs})/$",
        view=views.WorkListView.as_view(),
        name="work_list",
    ),
    re_path(
        rf"^(?P<kind_slug>{work_kind_slugs})/(?P<slug>[\w-]+)/$",
        view=views.WorkDetailView.as_view(),
        name="work_detail",
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/$",
        view=views.EventDetailView.as_view(),
        name="event_detail",
    ),
]
