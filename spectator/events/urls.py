from django.conf.urls import url

from . import views


# This should be under the namespace 'spectator:events'.

urlpatterns = [
    url(
        regex=r"^$",
        view=views.EventListView.as_view(),
        name='home'
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
        regex=r"^(?P<kind_slug>[-\w]+)/$",
        view=views.EventListView.as_view(),
        name='event_list'
    ),
    url(
        regex=r"^(?P<kind_slug>[-\w]+)/(?P<slug>[\w-]+)/$",
        view=views.EventDetailView.as_view(),
        name='event_detail'
    ),

    url(
        regex=r"^concerts/works/$",
        view=views.ClassicalWorkListView.as_view(),
        name='classicalwork_list'
    ),
    url(
        regex=r"^concerts/works/(?P<slug>[\w-]+)/$",
        view=views.ClassicalWorkDetailView.as_view(),
        name='classicalwork_detail'
    ),

    url(
        regex=r"^dance/pieces/$",
        view=views.DancePieceListView.as_view(),
        name='dancepiece_list'
    ),
    url(
        regex=r"^dance/pieces/(?P<slug>[\w-]+)/$",
        view=views.DancePieceDetailView.as_view(),
        name='dancepiece_detail'
    ),
]


