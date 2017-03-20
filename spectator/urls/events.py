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
        view=views.MovieEventListView.as_view(),
        name='movieevent_list',
    ),
    url(
        regex=r"^plays/$",
        view=views.PlayProductionEventListView.as_view(),
        name='playproductionevent_list',
    ),
]


