from django.conf.urls import (patterns,
                              url)

from bootstrap import urls as bootstrap_urls

from .forms import (AccountForm,
                    InventoryItemForm,
                    PurchaserForm,
                    TransactionForm)
from .models import InventoryItem
from .views import (MarkupDetailView,
                    CreateView)


urlpatterns = bootstrap_urls.bootstrap_patterns(AccountForm, InventoryItemForm, PurchaserForm)
urlpatterns += bootstrap_urls.bootstrap_pattern(TransactionForm, create_view=None)
urlpatterns += patterns(
    '',
    url(
        r'^transaction/add/$',
        CreateView.as_view(form_class=TransactionForm),
        name="transaction_form"
    ),
    url(
        r'^inventoryitem/(?P<pk>\d+)/json/$',
        MarkupDetailView.as_view(model=InventoryItem),
        name='inventoryitem_json',
    ),
)
