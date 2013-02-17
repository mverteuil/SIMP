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
    ## Accounts
    url(r'^a/$', 'inventory.views.accounts', name='accounts'),
    url(r'^a/(?P<account_id>\d+)/$',
        'inventory.views.account', name='account'),
    url(r'^a/create/$', 'inventory.views.account', name='account'),

    ## Inventory Items
    url(r'^i/$',
        'inventory.views.inventoryitems',
        name='inventoryitems'),

    url(r'^i/(?P<item_id>\d+)/$',
        'inventory.views.inventoryitem',
        {'editor': False},
        'inventoryitem_view'),

    url(r'^i/(?P<item_id>\d+)/edit/$',
        'inventory.views.inventoryitem',
        {'editor': True},
        'inventoryitem'),

    url(r'^i/create/$',
        'inventory.views.inventoryitem',
        {'editor': True},
        'inventoryitem'),

    ## Purchasers
    url(r'^p/$', 'inventory.views.purchasers', name='purchasers'),
    url(r'^p/(?P<p_id>\d+)/$', 'inventory.views.purchaser', name='purchaser'),
    url(r'^p/create/$', 'inventory.views.purchaser', name='purchaser'),

    ## Transactions
    url(r'^t/$', 'inventory.views.transactions', name='transactions'),
    url(r'^t/(?P<transact_id>\d+)/$',
        'inventory.views.transaction', name='transaction'),
    url(r'^t/(?P<transact_id>\d+)/delete/$',
        'inventory.views.delete_transaction', name='delete_transaction'),
    url(r'^t/create/$', 'inventory.views.transaction', name='transaction'),
)
