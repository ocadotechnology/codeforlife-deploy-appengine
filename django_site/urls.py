from django.conf.urls import include, url
from django.contrib import admin
from django_site.views import versions

from portal import urls as portal_urls
from game import urls as game_urls
from aimmo import urls as aimmo_urls
from reports import urls as reports_urls

js_info_dict = {"packages": ("conf.locale",)}

admin.autodiscover()

urlpatterns = [
    url(r"^", include(portal_urls)),
    url(r"^administration/", include(admin.site.urls)),
    url(r"^rapidrouter/", include(game_urls)),
    url(r"^reports/", include(reports_urls)),
    url(r"^aimmo/", include(aimmo_urls)),
    url(r"^versions/$", versions, name="versions"),
]
