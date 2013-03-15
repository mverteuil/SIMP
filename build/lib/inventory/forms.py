"""
    :platform: Unix, OS X
    :synopsis: Django forms for Inventory CRUD

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from django.forms import ModelForm

from inventory.models import Account
from inventory.models import InventoryItem
from inventory.models import Purchaser
from inventory.models import Transaction


class AccountForm(ModelForm):
    """
        Helper for creating and updating :class:`inventory.models.Account`
    """
    class Meta:
        model = Account


class InventoryItemForm(ModelForm):
    """
        Helper for creating and updating
        :class:`inventory.models.InventoryItem`
    """
    class Meta:
        model = InventoryItem


class PurchaserForm(ModelForm):
    """
        Helper for creating and updating :class:`inventory.models.Purchaser`
    """
    class Meta:
        model = Purchaser


class TransactionForm(ModelForm):
    """
        Helper for creating and updating :class:`inventory.models.Transaction`
    """
    class Meta:
        model = Transaction
