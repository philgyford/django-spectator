from django.contrib.sitemaps import Sitemap

from .models import Event, Venue


class EventSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        return Event.objects.all()

    def lastmod(self, obj):
        return obj.time_modified


class VenueSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Venue.objects.all()

    def lastmod(self, obj):
        return obj.time_modified

