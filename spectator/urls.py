from django.conf.urls import url

from . import views

urlpatterns = [
    url(
        regex=r"^$",
        view=views.HomeView.as_view(),
        name='home'
    ),
    # Individuals:
    url(
        regex=r"^creators/$",
        view=views.CreatorListView.as_view(),
        name='creator_list'
    ),
    #  Groupsa:
    url(
        regex=r"^creators/groups/$",
        view=views.CreatorListView.as_view(),
        name='creator_list_group',
        kwargs={'kind': 'group',}
    ),
    url(
        regex=r"^creators/(?P<pk>\d+)/$",
        view=views.CreatorDetailView.as_view(),
        name='creator_detail'
    ),
    url(
        regex=r"^reading/$",
        view=views.ReadingHomeView.as_view(),
        name='reading_home'
    ),
    url(
        regex=r"^reading/series/$",
        view=views.PublicationSeriesListView.as_view(),
        name='publicationseries_list'
    ),
    url(
        regex=r"^reading/series/(?P<pk>\d+)/$",
        view=views.PublicationSeriesDetailView.as_view(),
        name='publicationseries_detail'
    ),
    url(
        regex=r"^reading/publications/$",
        view=views.PublicationListView.as_view(),
        name='publication_list'
    ),
    url(
        regex=r"^reading/publications/periodicals/$",
        view=views.PublicationListView.as_view(),
        name='publication_list_periodical',
        kwargs={'kind': 'periodical',}
    ),
    url(
        regex=r"^reading/publications/(?P<pk>\d+)/$",
        view=views.PublicationDetailView.as_view(),
        name='publication_detail'
    ),
    url(
        regex=r"^reading/(?P<year>[0-9]{4})/$",
        view=views.ReadingYearArchiveView.as_view(),
        name='reading_year_archive'
    ),
]

