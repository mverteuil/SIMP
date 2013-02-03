"""
    :platform: Unix, OS X
    :synopsis: Django views for Inventory viewing & editing.

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from annoying.decorators import render_to

from inventory import forms
from inventory.models import Account
from inventory.models import InventoryItem
from inventory.models import Purchaser
from inventory.models import Transaction


@render_to('accounts.html')
def accounts(request):
    return dict(accounts=Account.objects.all())


@render_to('inventoryitems.html')
def inventoryitems(request):
    return dict(items=InventoryItem.objects.all())


@render_to('purchasers.html')
def purchasers(request):
    return dict(purchasers=Purchaser.objects.all())


@render_to('transactions.html')
def transactions(request):
    return dict(transactions=Transaction.objects.all())


@render_to('transaction.html')
def transaction(request, transact_id=None):
    data = request.POST if request.method == "POST" else None
    instance = Transaction.objects.get(pk=transact_id) if transact_id else None
    form = forms.TransactionForm(data, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('transactions'))
    return dict(form=form)
