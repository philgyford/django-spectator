from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        regex=r"^$",
        view=views.EventListView.as_view(),
        name='events_home'
    ),

    url(
        regex=r"^venues/$",
        view=views.VenueListView.as_view(),
        name='venue_list',
    ),
    url(
        regex=r"^venues/(?P<pk>\d+)/$",
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
        regex=r"^(?P<kind_slug>[-\w]+)/(?P<pk>\d+)/$",
        view=views.EventDetailView.as_view(),
        name='event_detail'
    ),

]


