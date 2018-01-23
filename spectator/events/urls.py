from django.conf.urls import url

from . import views
from .models import Event


app_name = 'events'

# Will be like 'movies|plays|concerts' etc:
kind_slugs = '|'.join(Event.get_valid_kind_slugs())

urlpatterns = [
    url(
        regex=r"^$",
        view=views.EventListView.as_view(),
        name='home'
    ),
    url(
        regex=r"^types/(?P<kind_slug>{})/$".format(kind_slugs),
        view=views.EventListView.as_view(),
        name='event_list'
    ),

    url(
        regex=r"^venues/$",
        view=views.VenueListView.as_view(),
        name='venue_list',
    ),
    url(
        regex=r"^venues/(?P<slug>[\w-]+)/$",
        view=views.VenueDetailView.as_view(),
        name='venue_detail'
    ),

    url(
        regex=r"^(?P<year>[0-9]{4})/$",
        view=views.EventYearArchiveView.as_view(),
        name='event_year_archive'
    ),

    url(
        regex=r"^movies/$",
        view=views.MovieListView.as_view(),
        name='movie_list'
    ),
    url(
        regex=r"^movies/(?P<slug>[\w-]+)/$",
        view=views.MovieDetailView.as_view(),
        name='movie_detail'
    ),

    url(
        regex=r"^plays/$",
        view=views.PlayListView.as_view(),
        name='play_list'
    ),
    url(
        regex=r"^plays/(?P<slug>[\w-]+)/$",
        view=views.PlayDetailView.as_view(),
        name='play_detail'
    ),

    url(
        regex=r"^classical-works/$",
        view=views.ClassicalWorkListView.as_view(),
        name='classicalwork_list'
    ),
    url(
        regex=r"^classical-works/(?P<slug>[\w-]+)/$",
        view=views.ClassicalWorkDetailView.as_view(),
        name='classicalwork_detail'
    ),

    url(
        regex=r"^dance-pieces/$",
        view=views.DancePieceListView.as_view(),
        name='dancepiece_list'
    ),
    url(
        regex=r"^dance-pieces/(?P<slug>[\w-]+)/$",
        view=views.DancePieceDetailView.as_view(),
        name='dancepiece_detail'
    ),

    url(
        regex=r"^(?P<slug>[\w-]+)/$",
        view=views.EventDetailView.as_view(),
        name='event_detail'
    ),

]
