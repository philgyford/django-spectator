from django.contrib.sitemaps import Sitemap

from .models import ClassicalWork, DancePiece, Event, Movie, Play, Venue


class ClassicalWorkSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return ClassicalWork.objects.all()

    def lastmod(self, obj):
        return obj.time_modified


class DancePieceSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return DancePiece.objects.all()

    def lastmod(self, obj):
        return obj.time_modified


class MovieSitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Movie.objects.all()

    def lastmod(self, obj):
        return obj.time_modified


class PlaySitemap(Sitemap):
    changefreq = 'monthly'
    priority = 0.5

    def items(self):
        return Play.objects.all()

    def lastmod(self, obj):
        return obj.time_modified


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

