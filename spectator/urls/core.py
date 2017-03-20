from django.conf.urls import include, url

from .. import views


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
    #  Groups:
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

    url(r'^events/', include('spectator.urls.events')),
    url(r'^reading/', include('spectator.urls.reading')),

]


