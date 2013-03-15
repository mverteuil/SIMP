from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from django.contrib import admin

from simp import settings

admin.autodiscover()

urlpatterns = patterns(
    '',

    # Django Admin URLs
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Documentation URLs
    url(r'^docs/$', 'django.views.static.serve',
        {'document_root': settings.DOCS_PATH, 'path': 'index.html'},
        name='docs'),
    url(r'^docs/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.DOCS_PATH}, name='docs'),
    # SIMP URLs
    url('^', include('inventory.urls', namespace='inventory'),)
)
