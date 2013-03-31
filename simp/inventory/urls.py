from bootstrap import urls as bootstrap_urls

from django.conf.urls import patterns, url


from .forms import (AccountForm,
                    InventoryItemForm,
                    PurchaserForm,
                    TransactionForm)
from .models import (InventoryItem,
                     Purchaser)
from .views import (MarkupDetailView,
                    CreateView,
                    ItemListView,
                    PurchaserListView)


urlpatterns = bootstrap_urls.bootstrap_patterns(AccountForm)
urlpatterns += bootstrap_urls.bootstrap_pattern(InventoryItemForm,
                                                list_view=None)
urlpatterns += bootstrap_urls.bootstrap_pattern(TransactionForm,
                                                create_view=None)
urlpatterns += bootstrap_urls.bootstrap_pattern(PurchaserForm,
                                                list_view=None)
urlpatterns += patterns(
    '',
    url(
        r'^inventoryitem/$',
        ItemListView.as_view(model=InventoryItem),
        name="inventoryitem_list"
    ),
    url(
        r'^inventoryitem/(?P<pk>\d+)/json/$',
        MarkupDetailView.as_view(model=InventoryItem),
        name='inventoryitem_json',
    ),
    url(
        r'^purchaser/$',
        PurchaserListView.as_view(model=Purchaser),
        name="purchaser_list"
    ),
    url(
        r'^transaction/add/$',
        CreateView.as_view(form_class=TransactionForm),
        name="transaction_form"
    ),
)
