from django.conf.urls import url

from .. import views


urlpatterns = [
    url(
        regex=r"^$",
        view=views.EventsHomeView.as_view(),
        name='events_home'
    ),
    url(
        regex=r"^concerts/$",
        view=views.ConcertListView.as_view(),
        name='concert_list',
    ),
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
        regex=r"^plays/$",
        view=views.PlayListView.as_view(),
        name='play_list',
    ),
    url(
        regex=r"^plays/visits/$",
        view=views.PlayProductionEventListView.as_view(),
        name='playproductionevent_list',
    ),
]


