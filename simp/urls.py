from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url

from django.contrib import admin

from simp import settings

from inventory.views import DeleteView
from inventory.views import MarkupDetailView
from inventory.views import SectionCreateView
from inventory.views import SectionDetailView
from inventory.views import SectionListView
from inventory.views import SectionUpdateView

from inventory import models


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
    url(r'^a/$',
        SectionListView.as_view(
            model=models.Account,
        ),
        name='account-list'),

    url(r'^a/create/$',
        SectionCreateView.as_view(
            model=models.Account,
            template_name="default_form.html",
        ),
        name='account-create'),

    url(r'^a/(?P<pk>\d+)/$',
        SectionDetailView.as_view(
            model=models.Account,
        ),
        name='account-details'),

    url(r'^a/(?P<pk>\d+)/update/$',
        SectionUpdateView.as_view(
            model=models.Account,
            template_name="default_form.html",
        ),
        name='account-update'),

    url(r'^a/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(
            model=models.Account
        ),
        name='account-delete'),

    ## Inventory Items
    url(r'^i/$',
        SectionListView.as_view(
            model=models.InventoryItem,
        ),
        name='inventoryitem-list'),

    url(r'^i/create/$',
        SectionCreateView.as_view(
            model=models.InventoryItem,
            template_name="default_form.html",
        ),
        name='inventoryitem-create'),

    url(r'^i/(?P<pk>\d+)/$',
        SectionDetailView.as_view(
            model=models.InventoryItem,
        ),
        name='inventoryitem-details'),

    url(r'^i/(?P<pk>\d+)/json/$',
        MarkupDetailView.as_view(
            model=models.InventoryItem,
        ),
        name='inventoryitem-json'),

    url(r'^i/(?P<pk>\d+)/update/$',
        SectionUpdateView.as_view(
            model=models.InventoryItem,
            template_name="default_form.html",
        ),
        name='inventoryitem-update'),

    url(r'^i/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(
            model=models.InventoryItem
        ),
        name='inventoryitem-delete'),

    ## Purchasers
    url(r'^p/$',
        SectionListView.as_view(
            model=models.Purchaser,
        ),
        name='purchaser-list'),

    url(r'^p/create/$',
        SectionCreateView.as_view(
            model=models.Purchaser,
            template_name="default_form.html",
        ),
        name='purchaser-create'),

    url(r'^p/(?P<pk>\d+)/$',
        SectionDetailView.as_view(
            model=models.Purchaser,
        ),
        name='purchaser-details'),

    url(r'^p/(?P<pk>\d+)/update/$',
        SectionUpdateView.as_view(
            model=models.Purchaser,
            template_name="default_form.html",
        ),
        name='purchaser-update'),

    url(r'^p/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(
            model=models.Purchaser
        ),
        name='purchaser-delete'),

    ## Transactions
    url(r'^t/$',
        SectionListView.as_view(
            model=models.Transaction,
        ),
        name='transaction-list'),

    url(r'^t/create/$',
        SectionCreateView.as_view(
            model=models.Transaction,
            template_name="inventory/transaction_form.html",
        ),
        name='transaction-create'),

    url(r'^t/(?P<pk>\d+)/$',
        SectionDetailView.as_view(
            model=models.Transaction,
        ),
        name='transaction-details'),

    url(r'^t/(?P<pk>\d+)/update/$',
        SectionUpdateView.as_view(
            model=models.Transaction,
            template_name="inventory/transaction_form.html",
        ),
        name='transaction-update'),

    url(r'^t/(?P<pk>\d+)/delete/$',
        DeleteView.as_view(
            model=models.Transaction
        ),
        name='transaction-delete'),
)
