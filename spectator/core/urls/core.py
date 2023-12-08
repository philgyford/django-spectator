from django.urls import path

from spectator.core import views

# Only the home page.
# This should be under the namespace 'spectator:core'.

app_name = "core"

urlpatterns = [
    path("", view=views.HomeView.as_view(), name="home"),
]
