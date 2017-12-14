from django.conf.urls import include, url

from ..apps import spectator_apps


# The aim of this is to:
# a) Make it easy to include Spectator's URLs in a project with a single line.
# b) Also make it easy to only include parts of the project, if necessary.

app_name='spectator'

urlpatterns = [
    url(r'^', include('spectator.core.urls.core')),

    url(r'^creators/', include('spectator.core.urls.creators')),
]

if spectator_apps.is_enabled('events'):
    urlpatterns.append(
        url(r'^events/', include('spectator.events.urls', namespace='events')),
    )

if spectator_apps.is_enabled('reading'):
    urlpatterns.append(
        url(r'^reading/', include('spectator.reading.urls', namespace='reading')),
    )
