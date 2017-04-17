from django.conf.urls import url

from .. import views


# Only the home page.
# This should be under the namespace 'spectator:core'.

urlpatterns = [
    url(
        regex=r"^$",
        view=views.HomeView.as_view(),
        name='home'
    ),
]

