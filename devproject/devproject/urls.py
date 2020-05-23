from django.conf import settings
from django.conf.urls import include, static, url
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap

from spectator.core.apps import spectator_apps
from spectator.core.sitemaps import CreatorSitemap

if spectator_apps.is_enabled("events"):
    from spectator.events.sitemaps import EventSitemap, VenueSitemap, WorkSitemap

if spectator_apps.is_enabled("reading"):
    from spectator.reading.sitemaps import PublicationSitemap, PublicationSeriesSitemap


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
    url(r"^admin/", admin.site.urls),
    url(r"^", include("spectator.core.urls")),
    url(
        r"^sitemap\.xml$",
        sitemap,
        {"sitemaps": sitemaps},
        name="django.contrib.sitemaps.views.sitemap",
    ),
]


if settings.DEBUG:

    import debug_toolbar

    urlpatterns += [
        url(r"^__debug__/", include(debug_toolbar.urls)),
    ]

    urlpatterns += static.static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    urlpatterns += static.static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
