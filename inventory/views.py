"""
    :platform: Unix, OS X
    :synopsis: Django views for Inventory viewing & editing.

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
import json

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from annoying.decorators import render_to

from inventory import forms
from inventory.models import Account
from inventory.models import InventoryItem
from inventory.models import Purchaser
from inventory.models import Transaction


def generate_markup_map():
    """
        Produces a dict mapping (id, markup) for
        using the markup_scheme field data of items in JavaScript
        functions

        Returns
        -------
        markup_map : `dict`
            A dicts {'1': '1@1'}
    """
    return dict((i.pk, i.markup_scheme,) for i in InventoryItem.objects.all())


@render_to('account.html')
def account(request, p_id=None):
    data = request.POST if request.method == "POST" else None
    instance = Account.objects.get(pk=p_id) if p_id else None
    form = forms.AccountForm(data, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('accounts'))
    return dict(form=form)


@render_to('accounts.html')
def accounts(request):
    return dict(accounts=Account.objects.all())


@render_to('inventoryitem.html')
def inventoryitem(request, item_id=None, editor=False):
    instance = InventoryItem.objects.get(pk=item_id) if item_id else None
    if editor:
        data = request.POST if request.method == "POST" else None
        form = forms.InventoryItemForm(data, instance=instance)
        if request.method == "POST":
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('inventoryitems'))
        return dict(form=form)
    else:
        return dict(item=instance)


@render_to('inventoryitems.html')
def inventoryitems(request):
    return dict(items=InventoryItem.objects.all())


@render_to('purchaser.html')
def purchaser(request, p_id=None):
    data = request.POST if request.method == "POST" else None
    instance = Purchaser.objects.get(pk=p_id) if p_id else None
    form = forms.PurchaserForm(data, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('purchasers'))
    return dict(form=form)


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
    return dict(form=form,
                items=json.dumps(generate_markup_map()))
