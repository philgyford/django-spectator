from django.contrib.sitemaps import Sitemap

from .models import Publication, PublicationSeries


class PublicationSitemap(Sitemap):
    changefreq = "yearly"
    priority = 0.5

    def items(self):
        return Publication.visible_objects.all()

    def lastmod(self, obj):
        return obj.time_modified


class PublicationSeriesSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return PublicationSeries.visible_objects.all()

    def lastmod(self, obj):
        return obj.time_modified
