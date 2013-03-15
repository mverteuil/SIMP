from django.conf.urls import patterns
from django.conf.urls import url

from bootstrap.urls import bootstrap_patterns

from .forms import AccountForm
from .forms import InventoryItemForm
from .forms import PurchaserForm
from .forms import TransactionForm

from .models import InventoryItem
from .views import MarkupDetailView


urlpatterns = bootstrap_patterns(AccountForm)
urlpatterns += bootstrap_patterns(InventoryItemForm)
urlpatterns += bootstrap_patterns(PurchaserForm)
urlpatterns += bootstrap_patterns(TransactionForm)
urlpatterns += patterns(
    '',
    url(
        r'^inventoryitem/(?P<pk>\d+)/json/$',
        MarkupDetailView.as_view(model=InventoryItem),
        name='inventoryitem_json',
    ),
)
