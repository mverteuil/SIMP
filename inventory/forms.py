"""
    :platform: Unix, OS X
    :synopsis: Django forms for Inventory CRUD

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from django.forms import ModelForm

from inventory.models import Transaction


class TransactionForm(ModelForm):
    """
        Helper for creating and updating :class:`inventory.models.Transaction`
    """
    class Meta:
        model = Transaction
