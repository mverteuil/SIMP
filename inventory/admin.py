from django.contrib import admin

from inventory.models import Account
from inventory.models import InventoryItem
from inventory.models import Purchaser
from inventory.models import Transaction

admin.site.register(Account)
admin.site.register(InventoryItem)
admin.site.register(Purchaser)
admin.site.register(Transaction)
