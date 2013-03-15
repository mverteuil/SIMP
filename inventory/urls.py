from bootstrap.urls import bootstrap_patterns

from .forms import AccountForm
from .forms import InventoryItemForm
from .forms import PurchaserForm
from .forms import TransactionForm


urlpatterns = bootstrap_patterns(AccountForm)
urlpatterns += bootstrap_patterns(InventoryItemForm)
urlpatterns += bootstrap_patterns(PurchaserForm)
urlpatterns += bootstrap_patterns(TransactionForm)
