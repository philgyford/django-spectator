from django.conf.urls import include, static, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^', include('spectator.core.urls', namespace='spectator_core')),

    url(r'^events/', include('spectator.events.urls',
                                            namespace='spectator_events')),

    url(r'^reading/', include('spectator.reading.urls',
                                            namespace='spectator_reading')),
]


from django.conf import settings

if settings.DEBUG:

    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]

    urlpatterns += \
        static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += \
        static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

