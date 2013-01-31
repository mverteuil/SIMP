from annoying.decorators import render_to

from inventory import models as inventory


@render_to('accounts.html')
def accounts(request):
    def balancer():
        for account in inventory.Account.objects.all():
            balance = sum([t.delta_balance for t in inventory.Transaction.objects.filter(account=account)])
            balance += account.initial_balance
            yield (account, balance,)
    accounts = list(balancer())
    return dict(accounts=accounts)


@render_to('inventory_list.html')
def inventory_list(request):
    def itemizer():
        for item in inventory.InventoryItem.objects.all():
            quantity = sum([t.delta_quantity for t in inventory.Transaction.objects.filter(item=item)])
            yield (item, quantity,)
    items = list(itemizer())
    return dict(items=items)


@render_to('purchasers.html')
def purchasers(request):
    def purchasizer(purchaser):
        balance = 0
        for account in inventory.Account.objects.all():
            balance += sum([t.delta_balance for t in inventory.Transaction.objects.filter(purchaser=purchaser)])
        return balance

    def generatizer(purchaser):
        quantity = 0
        for item in inventory.InventoryItem.objects.all():
            quantity += sum([abs(t.delta_quantity) for t in inventory.Transaction.objects.filter(purchaser=purchaser)])
        return quantity

    purchasers = [(p, generatizer(p), purchasizer(p),) for p in inventory.Purchaser.objects.all()]
    return dict(purchasers=purchasers)
