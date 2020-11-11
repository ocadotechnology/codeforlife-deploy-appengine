from aimmo import urls as aimmo_urls
from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from game import urls as game_urls
from portal import urls as portal_urls

from django_site.views import versions

js_info_dict = {"packages": ("conf.locale",)}

admin.autodiscover()

urlpatterns = [
    url(r"^", include(portal_urls)),
    path("admin/", admin.site.urls),
    url(r"^rapidrouter/", include(game_urls)),
    url(r"^kurono/", include(aimmo_urls)),
    url(r"^versions/$", versions, name="versions"),
]
