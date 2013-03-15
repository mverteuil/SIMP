from django.contrib import admin

from .models import Account
from .models import InventoryItem
from .models import Purchaser
from .models import Transaction

admin.site.register(Account)
admin.site.register(InventoryItem)
admin.site.register(Purchaser)
admin.site.register(Transaction)
