from django.conf.urls import url

from . import views
from .models import Event, Work


app_name = 'events'

# Will be like 'movies|plays|concerts' etc:
event_kind_slugs = '|'.join(Event.get_valid_kind_slugs())

# Will be like 'classical-works|dance-pieces' etc:
work_kind_slugs = '|'.join(Work.get_valid_kind_slugs())

urlpatterns = [
    url(
        regex=r"^$",
        view=views.EventListView.as_view(),
        name='home'
    ),
    url(
        regex=r"^types/(?P<kind_slug>{})/$".format(event_kind_slugs),
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
        regex=r"^(?P<kind_slug>{})/$".format(work_kind_slugs),
        view=views.WorkListView.as_view(),
        name='work_list'
    ),
    url(
        regex=r"^(?P<kind_slug>{})/(?P<slug>[\w-]+)/$".format(work_kind_slugs),
        view=views.WorkDetailView.as_view(),
        name='work_detail'
    ),

    url(
        regex=r"^(?P<slug>[\w-]+)/$",
        view=views.EventDetailView.as_view(),
        name='event_detail'
    ),

]
