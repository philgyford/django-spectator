from django.conf.urls import url

from .. import views


app_name = 'creators'

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
        regex=r"^(?P<slug>[\w-]+)/$",
        view=views.CreatorDetailView.as_view(),
        name='creator_detail'
    ),
]

