from django.urls import include, path

from spectator.core.apps import spectator_apps

# The aim of this is to:
# a) Make it easy to include Spectator's URLs in a project with a single line.
# b) Also make it easy to only include parts of the project, if necessary.

app_name = "spectator"

urlpatterns = [
    path("", include("spectator.core.urls.core")),
    path("creators/", include("spectator.core.urls.creators")),
]

if spectator_apps.is_enabled("events"):
    urlpatterns.append(
        path("events/", include("spectator.events.urls", namespace="events")),
    )

if spectator_apps.is_enabled("reading"):
    urlpatterns.append(
        path("reading/", include("spectator.reading.urls", namespace="reading")),
    )
