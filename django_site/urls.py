from lib.django.conf.urls import include, url
from lib.django.contrib import admin
from lib.django_site.views import versions

from lib.portal import urls as portal_urls
from lib.game import urls as game_urls
from lib.aimmo import urls as aimmo_urls

js_info_dict = {"packages": ("conf.locale",)}

admin.autodiscover()

urlpatterns = [
    url(r"^", include(portal_urls)),
    url(r"^administration/", include(admin.site.urls)),
    url(r"^rapidrouter/", include(game_urls)),
    url(r"^kurono/", include(aimmo_urls)),
    url(r"^versions/$", versions, name="versions"),
]
