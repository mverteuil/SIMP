from annoying.decorators import render_to

from inventory import models as inventory


@render_to('inventory_list.html')
def inventory_list(request):
    def itemizer():
        for item in inventory.InventoryItem.objects.all():
            quantity = sum([t.delta_quantity for t in inventory.Transaction.objects.filter(item=item)])
            yield (item, quantity,)
    items = list(itemizer())
    return dict(items=items)


@render_to('accounts.html')
def accounts(request):
    def balancer():
        for account in inventory.Account.objects.all():
            balance = sum([t.delta_balance for t in inventory.Transaction.objects.filter(account=account)])
            balance += account.initial_balance
            yield (account, balance,)
    accounts = list(balancer())
    return dict(accounts=accounts)
