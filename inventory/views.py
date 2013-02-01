from annoying.decorators import render_to

from inventory import models as inventory


@render_to('accounts.html')
def accounts(request):
    return dict(accounts=inventory.Account.objects.all())


@render_to('inventory_list.html')
def inventory_list(request):
    return dict(items=inventory.InventoryItem.objects.all())


@render_to('purchasers.html')
def purchasers(request):
    return dict(purchasers=inventory.Purchaser.objects.all())
