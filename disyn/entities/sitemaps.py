from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Entity

class EntitySitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Entity.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['entity_list', 'apply']

    def location(self, item):
        return reverse(item)