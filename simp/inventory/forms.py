"""
    :platform: Unix, OS X
    :synopsis: Django forms for Inventory CRUD

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from django import forms

from .models import (Account,
                     InventoryItem,
                     Purchaser,
                     Transaction)


class AccountForm(forms.ModelForm):
    """
        Helper for creating and updating :class:`.models.Account`
    """
    class Meta:
        model = Account


class InventoryItemForm(forms.ModelForm):
    """
        Helper for creating and updating
        :class:`simp.inventory.models.InventoryItem`
    """
    class Meta:
        model = InventoryItem


class PurchaserForm(forms.ModelForm):
    """
        Helper for creating and updating :class:`.models.Purchaser`
    """
    class Meta:
        model = Purchaser


class TransactionForm(forms.ModelForm):
    """
        Helper for creating and updating :class:`.models.Transaction`
    """
    class Meta:
        model = Transaction
    item = forms.ModelChoiceField(required=True,
                                  queryset=InventoryItem.objects.exclude(
                                      archived=True))
    account = forms.ModelChoiceField(required=True,
                                     queryset=Account.objects.exclude(
                                         archived=True))
    purchaser = forms.ModelChoiceField(required=True,
                                       queryset=Purchaser.objects.exclude(
                                           archived=True))
