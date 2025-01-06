from django.urls import path, re_path

from spectator.core import views

app_name = "creators"

urlpatterns = [
    # Individuals:
    path("", view=views.CreatorListView.as_view(), name="creator_list"),
    #  Groups:
    path(
        "groups/",
        view=views.CreatorListView.as_view(),
        name="creator_list_group",
        kwargs={"kind": "group"},
    ),
    re_path(
        r"^(?P<slug>[\w-]+)/$",
        view=views.CreatorDetailView.as_view(),
        name="creator_detail",
    ),
]
