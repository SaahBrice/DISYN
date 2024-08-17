from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from entities.sitemaps import EntitySitemap, StaticViewSitemap
from django.contrib.sitemaps.views import sitemap


sitemaps = {
    'entities': EntitySitemap,
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('entities.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)