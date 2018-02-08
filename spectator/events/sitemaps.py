from django.contrib.sitemaps import Sitemap

from .models import Event, Venue, Work


class EventSitemap(Sitemap):
    changefreq = 'never'
    priority = 0.5

    def items(self):
        # Exclude movies and plays because they'll have the same URLs as their
        # Movie and Play objects.
        return Event.objects.exclude(kind='movie')\
                            .exclude(kind='play')

    def lastmod(self, obj):
        return obj.time_modified


class VenueSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Venue.objects.all()

    def lastmod(self, obj):
        return obj.time_modified


class WorkSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Work.objects.all()

    def lastmod(self, obj):
        return obj.time_modified
