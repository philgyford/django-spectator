from django.urls import path, re_path

from . import views

app_name = "reading"

urlpatterns = [
    path("", view=views.ReadingHomeView.as_view(), name="home"),
    path(
        "series/",
        view=views.PublicationSeriesListView.as_view(),
        name="publicationseries_list",
    ),
    re_path(
        r"^series/(?P<slug>[\w-]+)/$",
        view=views.PublicationSeriesDetailView.as_view(),
        name="publicationseries_detail",
    ),
    path(
        "publications/",
        view=views.PublicationListView.as_view(),
        name="publication_list",
    ),
    path(
        "publications/periodicals/",
        view=views.PublicationListView.as_view(),
        name="publication_list_periodical",
        kwargs={"kind": "periodical"},
    ),
    re_path(
        r"^publications/(?P<slug>[\w-]+)/$",
        view=views.PublicationDetailView.as_view(),
        name="publication_detail",
    ),
    re_path(
        r"^(?P<year>[0-9]{4})/$",
        view=views.ReadingYearArchiveView.as_view(),
        name="reading_year_archive",
    ),
    re_path(
        r"^(?P<year>[0-9]{4})/(?P<kind>[\w-]+)/$",
        view=views.ReadingYearArchiveView.as_view(),
        name="reading_year_archive",
    ),
]
