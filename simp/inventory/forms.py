"""
    :platform: Unix, OS X
    :synopsis: Django forms for Inventory CRUD

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from django.forms import ModelForm

from simp.inventory.models import Account
from simp.inventory.models import InventoryItem
from simp.inventory.models import Purchaser
from simp.inventory.models import Transaction


class AccountForm(ModelForm):
    """
        Helper for creating and updating :class:`simp.inventory.models.Account`
    """
    class Meta:
        model = Account


class InventoryItemForm(ModelForm):
    """
        Helper for creating and updating
        :class:`simp.inventory.models.InventoryItem`
    """
    class Meta:
        model = InventoryItem


class PurchaserForm(ModelForm):
    """
        Helper for creating and updating :class:`simp.inventory.models.Purchaser`
    """
    class Meta:
        model = Purchaser


class TransactionForm(ModelForm):
    """
        Helper for creating and updating :class:`simp.inventory.models.Transaction`
    """
    class Meta:
        model = Transaction
