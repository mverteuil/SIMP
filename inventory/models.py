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

    @property
    def acquired(self):
        """
            Find dates corresponding to inbound transactions

            Returns
            -------
            acquired_dates : `list`
        """
        return [t.timestamp for t in self.inbound_transactions]

    def calculate_quantity(self):
        """
            Calculates the current quantity by summing transactions

            Returns
            -------
            quantity : `float`
                The calculated quantity
        """
        return sum([t.delta_quantity for t in self.transactions.all()])

    def calculate_purchased_value_per_unit(self):
        """
            Calculates the current determined value per unit based solely on
            the rates at which this item was acquired.

            For example:
                Apples were stocked twice, first we acquired 75@50.00, then
                we acquired 270@150 later. in the first acquisition we have a
                value/unit rate of 50/75=0.66, in the second the rate is
                150/270=0.55. so we'll return the mean rate of 0.66+0.55/2=0.61

            returns
            -------
            purchased_value_per_unit : :class:`decimal.Decimal`
                The mean of calculated cost/unit values where we are
                the purchaser
        """
        vpus = [(abs(t.delta_balance) / D(t.delta_quantity)) for t in
                self.inbound_transactions]
        return sum(vpus) / (max(len(vpus), 1))

    def calculate_sold_value_per_unit(self):
        """
            Calculates the current determined value per unit based solely on
            the rates at which this item was sold.

            For example:
                Apples were sold twice, first we sold 75@50.00, then
                we sold 270@150 later. In the first sale we have a
                value/unit rate of 50/75=0.66, in the second the rate is
                150/270=0.55. So we'll return the mean rate of 0.66+0.55/2=0.61

            Returns
            -------
            sold_value_per_unit : :class:`decimal.Decimal`
                The mean of calculated cost/unit values where we are
                the seller
        """
        vpus = [(t.delta_balance / D(abs(t.delta_quantity))) for t in
                self.outbound_transactions]
        return sum(vpus) / (max(len(vpus), 1))

    @property
    def inbound_transactions(self):
        """
            Transactions where the quantity is greater than zero.

            Returns
            -------
            inbound_transactions : list
                A list of transactions where delta_quantity > 0.
        """
        return self.transactions.filter(delta_quantity__gt=0)

    @property
    def outbound_transactions(self):
        """
            Transactions where the quantity is equal to or less than zero.

            Returns
            -------
            outbound_transactions : list
                A list of transactions where delta_quantity <= 0.
        """
        return self.transactions.filter(delta_quantity__lte=0)


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

    def calculate_balance(self):
        """
            Calculates the current balance by summing transactions with
            the initial balance.

            Returns
            -------
            balance : :class:`decimal.Decimal`
                The calculated balance
        """
        balance = sum([t.delta_balance for t in
                       Transaction.objects.filter(account=self)])
        return self.initial_balance + balance


class Transaction(models.Model):
    """
        Represents a transaction and tracks the changes in quantities and
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
        return "%s | %s | %s | %s | %s@%s" % (self.timestamp,
                                              self.transaction_code,
                                              self.account.name,
                                              self.item.name,
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

    def calculate_income(self):
        """
            Sums the transaction balances where this purchaser was the buyer

            Returns
            -------
            calculated_income : :class:`decimal.Decimal`
                The sum of transaction.delta_balance for which this purchaser
                was the buyer
        """
        return sum([t.delta_balance for t in
                    Transaction.objects.filter(purchaser=self)
                    if t.delta_balance > 0])

    def calculate_consumption(self):
        """
            Sums the transaction quantities where this purchaser was the buyer

            Returns
            -------
            calculated_consumption : `float`
                The sume of transaction.delta_quantity for which this purchaser
                was the buyer
        """
        return abs(sum([t.delta_quantity for t in
                        Transaction.objects.filter(purchaser=self)
                        if t.delta_quantity < 0]))
