from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from spectator.core.apps import spectator_apps
from spectator.core.sitemaps import CreatorSitemap

if spectator_apps.is_enabled("events"):
    from spectator.events.sitemaps import EventSitemap, VenueSitemap, WorkSitemap

if spectator_apps.is_enabled("reading"):
    from spectator.reading.sitemaps import PublicationSeriesSitemap, PublicationSitemap


sitemaps = {
    "creators": CreatorSitemap,
}

if spectator_apps.is_enabled("events"):
    sitemaps["events"] = EventSitemap
    sitemaps["works"] = WorkSitemap
    sitemaps["venues"] = VenueSitemap

if spectator_apps.is_enabled("reading"):
    sitemaps["publications"] = PublicationSitemap
    sitemaps["publicationseries"] = PublicationSeriesSitemap


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("spectator.core.urls")),
    path(
        "sitemap.xml",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]


if settings.DEBUG:

    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
