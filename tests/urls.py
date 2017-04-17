from django.conf.urls import include, url
from django.contrib import admin


urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'', include('spectator.core.urls', namespace='spectator_core')),

    url(r'^events/', include('spectator.events.urls',
                                            namespace='spectator_events')),

    url(r'^reading/', include('spectator.reading.urls',
                                            namespace='spectator_reading')),
]

