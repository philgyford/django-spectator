from django.conf.urls import url

from .. import views


urlpatterns = [
    url(
        regex=r"^events/$",
        view=views.EventsHomeView.as_view(),
        name='events_home'
    ),
]


