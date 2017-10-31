from django.contrib.sitemaps import Sitemap

from .models import Creator


class CreatorSitemap(Sitemap):
    changefreq = 'yearly'
    priority = 0.5

    def items(self):
        return Creator.objects.all()

    def lastmod(self, obj):
        return obj.time_modified

