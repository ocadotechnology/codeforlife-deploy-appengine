from django.conf.urls import include, url
from django.contrib import admin

from django_site.views import versions

js_info_dict = {
    'packages': ('conf.locale',),
}

admin.autodiscover()

urlpatterns = [
    '',
    url(r'^', include('portal.urls')),
    url(r'^administration/', include(admin.site.urls)),
    url(r'^rapidrouter/', include('game.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^aimmo/', include('aimmo.urls')),
    url(r'^versions/$', versions, name='versions')
]

try:
    import django_pandasso
    urlpatterns = urlpatterns + patterns(url(r'^django-pandasso/', include('django_pandasso.urls')))
except ImportError:
    pass
