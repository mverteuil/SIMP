"""
    :platform: Unix, OS X
    :synopsis: Django views for Inventory viewing & editing.

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from annoying.decorators import render_to

from inventory import forms
from inventory.models import Account
from inventory.models import InventoryItem
from inventory.models import Purchaser


@render_to('accounts.html')
def accounts(request):
    return dict(accounts=Account.objects.all())


@render_to('inventoryitems.html')
def inventoryitems(request):
    return dict(items=InventoryItem.objects.all())


@render_to('purchasers.html')
def purchasers(request):
    return dict(purchasers=Purchaser.objects.all())
