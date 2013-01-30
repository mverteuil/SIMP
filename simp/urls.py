from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'SIMP.views.home', name='home'),
    # url(r'^SIMP/', include('SIMP.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^a/', 'inventory.views.accounts', name='accounts'),
    url(r'^i/', 'inventory.views.inventory_list', name='inventory_list'),
)