from django.conf.urls import url

from .. import views

# All Creator-specific URLs, so they can be included under whatever path is
# required.
# This should be under the namespace 'spectator:creators'.

urlpatterns = [
    # Individuals:
    url(
        regex=r"^$",
        view=views.CreatorListView.as_view(),
        name='creator_list'
    ),
    #  Groups:
    url(
        regex=r"^groups/$",
        view=views.CreatorListView.as_view(),
        name='creator_list_group',
        kwargs={'kind': 'group',}
    ),
    url(
        regex=r"^(?P<pk>\d+)/$",
        view=views.CreatorDetailView.as_view(),
        name='creator_detail'
    ),
]

