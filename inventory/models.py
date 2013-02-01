"""
    :platform: Unix, OS X
    :synopsis: Django ORMDB Inventory models

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from decimal import Decimal as D

from django.db import models


class InventoryItem(models.Model):
    """
        Represents a specific inventory item. For example, an fruit store would
        probably have entries for "Banana", "Apple", "Grapefruit", etc.

        Parameters
        ----------
        name : `string`
            A human readable name for this item
        markup_scheme : `string`
            A format string, with the syntax--
               `{quantity}@{price}[, {quantity}@{price}, ...]`
            Used to set up pricing 'tiers', as in the case: *Apples are $1.00
            each, but we sell 5 Apples for $4.00.* Which would be represented
            in as::
                1@1.00,5@4.00

    """
    name = models.CharField(verbose_name="Name",
                            max_length=64,
                            blank=False)
    markup_scheme = models.CharField(verbose_name="Markup Scheme",
                                     max_length=64,
                                     blank=True)

    def __unicode__(self):
        return self.name


class Account(models.Model):
    """
        Represents a 'wallet', so to speak. A pool of money used to purchase
        supplies and receive income. Generally speaking you will probably have
        only one 'Main' account unless your needs are particularly special.

        Parameters
        ----------
        name : `string`
            A human readable name for this item
        initial_balance : :class:`decimal.Decimal`
            The initial cash balance of the account before any transactions
            have taken place.
    """
    name = models.CharField(verbose_name="Name",
                            max_length=64,
                            blank=False)
    initial_balance = models.DecimalField(verbose_name="Initial Balance",
                                          max_digits=8,
                                          decimal_places=2,
                                          default=D('0.00'))

    def __unicode__(self):
        return self.name


class Transaction(models.Model):
    """
        represents a transaction and tracks the changes in quantities and 
        balance over time, storing the name of the purchaser too, if this is an
        inventory-outbound transaction.

        Parameters
        ----------
        item : :class:`InventoryItem`
            The item this transaction concerns
        account : :class:`Account`
            Where the money will come from or go
        purchaser : :class:`Purchaser`
            Who we're buying from or selling to
        delta_quantity : `float`
            Negative quantities for sale, positive for purchase
        delta_balance : :class:`decimal.Decimal`
            Negative quantities for purchase, positive for sale
        timestamp : :class:`datetime.datetime`
            The time/date of the transaction completion
    """
    item = models.ForeignKey("InventoryItem",
                             related_name="transactions",
                             null=True)
    account = models.ForeignKey("Account",
                                related_name="transactions",
                                null=True)
    purchaser = models.ForeignKey("Purchaser",
                                  related_name="transactions",
                                  null=True,
                                  blank=True)
    delta_quantity = models.FloatField(verbose_name="Delta Quantity",
                                       default=0.0)
    delta_balance = models.DecimalField(verbose_name="Delta Balance",
                                        max_digits=8,
                                        decimal_places=2,
                                        default=D('0.00'))
    timestamp = models.DateTimeField(verbose_name="Timestamp",
                                     auto_now_add=True)

    @property
    def transaction_code(self):
        if self.delta_balance < 0:
            return "INB"
        elif self.delta_balance == 0:
            return "NIL"
        else:
            return "OUT"

    def __unicode__(self):
        return "%s | %s | %s | %s@%s" % (self.transaction_code,
                                         self.account.name, self.item.name,
                                         self.delta_quantity,
                                         self.delta_balance)


class Purchaser(models.Model):
    """
        Represents a buyer or seller in transactions.

        Parameters
        ----------
        name : `string`
            A human readable name for this item
    """
    name = models.CharField(verbose_name="Name",
                            max_length=64,
                            blank=False)

    def __unicode__(self):
        return self.name
