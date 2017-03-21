from django.conf.urls import url

from .. import views


urlpatterns = [
    url(
        regex=r"^$",
        view=views.EventsHomeView.as_view(),
        name='events_home'
    ),

    # CONCERTS

    url(
        regex=r"^concerts/$",
        view=views.ConcertListView.as_view(),
        name='concert_list',
    ),
    # There aren't any "ConcertEvents"; this is really just a different view
    # of Concert objects:
    url(
        regex=r"^concerts/visits/$",
        view=views.ConcertEventListView.as_view(),
        name='concertevent_list',
    ),
    url(
        regex=r"^concerts/(?P<pk>\d+)/$",
        view=views.ConcertDetailView.as_view(),
        name='concert_detail'
    ),

    # MOVIES

    url(
        regex=r"^movies/$",
        view=views.MovieListView.as_view(),
        name='movie_list',
    ),
    url(
        regex=r"^movies/visits/$",
        view=views.MovieEventListView.as_view(),
        name='movieevent_list',
    ),
    url(
        regex=r"^movies/(?P<pk>\d+)/$",
        view=views.MovieDetailView.as_view(),
        name='movie_detail'
    ),

    # PLAYS

    url(
        regex=r"^plays/$",
        view=views.PlayListView.as_view(),
        name='play_list',
    ),
    url(
        regex=r"^plays/visits/$",
        view=views.PlayProductionEventListView.as_view(),
        name='playproductionevent_list',
    ),
    url(
        regex=r"^plays/(?P<pk>\d+)/$",
        view=views.PlayDetailView.as_view(),
        name='play_detail'
    ),
]


