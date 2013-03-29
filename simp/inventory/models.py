"""
    :platform: Unix, OS X
    :synopsis: Django ORMDB Inventory models

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from decimal import Decimal as D
from math import ceil

from django.core.urlresolvers import reverse
from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models


class InventoryItem(models.Model):
    """
        Represents a specific inventory item. For example, an fruit store would
        probably have entries for "Banana", "Apple", "Grapefruit", etc.

        Pricing is determined as follows:
            Acquired: 250 units @ $1500.00
            Decay: 2, Growth: 6%, Nearest: 5
                                 250 units @1500.00
            125 units @ 750.00 > 125 units @ 800.00
             62 units @ 400.00 >  62 units @ 430.00
             31 units @ 215.00 >  31 units @ 230.00
             15 units @ 115.00 >  15 units @ 125.00
              7 units @  62.50 >   7 units @  70.00
              3 units @  30.00 >   3 units @  35.00
              1  unit @  13.33 >   1  unit @  15.00

        Parameters
        ----------
        name : `string`
            A human readable name for this item
        markup_decay : `int`
            The rate at which growth is applied to prices which are
            marked up on a sliding scale with more profit made on
            lower units purchased. A faster growth occurs when this
            number is smaller. A reasonable decay is 2.
        markup_growth : `float`
            The rate at which to grow at each interval introduced by
            the decay. A modest rate is 6% or 1.06.
        markup_nearest : `int`
            Always round up to the nearest whole ones value within the domain
            of multiples of this number. Default is 5.
    """
    name = models.CharField(verbose_name="Name",
                            max_length=64,
                            blank=False)
    markup_decay = models.PositiveIntegerField(verbose_name="Markup Decay",
                                               default=2,)
    markup_growth = models.FloatField(verbose_name="Markup Growth",
                                      default=1.06,
                                      validators=[
                                          MinValueValidator(1)
                                      ],)
    markup_nearest = models.PositiveIntegerField(verbose_name="Markup Nearest",
                                                 default=5,
                                                 validators=[
                                                     MinValueValidator(0),
                                                     MaxValueValidator(9)
                                                 ],)

    class Meta:
        verbose_name = "Item"
        verbose_name_plural = "Items"

    @classmethod
    def get_list_url(self):
        return reverse('inventory:inventoryitem_list')

    def get_absolute_url(self):
        return reverse('inventory:inventoryitem_detail',
                       kwargs=dict(pk=self.pk))

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
        return max(0, sum(t.delta_quantity for t in self.transactions.all()))

    def calculate_purchased_value_per_unit(self):
        """
            Calculates the current determined value per unit based solely on
            the rates at which this item was acquired.

            For example:
                Apples were stocked twice, first we acquired 50 @ 0.25 = 12.50.
                We acquired 50 @ 0.30 = 15.00 later. A grand total of 27.50 is
                spent, with 100 units acquired, so the value per unit is 0.275.
                (27.50 spent/100 units acquired)

            Returns
            -------
            purchased_value_per_unit : :class:`decimal.Decimal`
                The mean of calculated cost/unit values where we are
                the purchaser
        """
        total = sum((abs(t.delta_balance) for t in self.inbound_transactions))
        return total / D(max(self.total_acquired, 1))

    def calculate_sold_value_per_unit(self):
        """
            Calculates the current determined value per unit based solely on
            the rates at which this item was sold.

            For example:
                Apples were sold four times, first we sold 25@0.50, then
                we sold 50@0.40 later. Next we have two sales, at 0.70, one
                of 12 and one of 13. A grand total of 50.00 is earned, with 100
                units sold, so the sold value per unit is 0.50.
                (50.00 earned/100 units sold)

            Returns
            -------
            sold_value_per_unit : :class:`decimal.Decimal`
                The mean of calculated cost/unit values where we are
                the seller
        """
        total = sum(abs(t.delta_balance) for t in self.outbound_transactions)
        return total / D(max(self.total_sold, 1))

    def calculate_potential_value(self):
        """
            Calculates the current potential value of this item.

            Potential value is:
                (total acquired) x (sold value per unit)

            Returns
            -------
            potential : :class:`decimal.Decimal`
                The amount this item is potentially worth, given its history
        """
        return D(self.total_acquired) * self.calculate_sold_value_per_unit()

    def calculate_shrink_at_cost(self):
        """
            Calculates the amount lost to shrink at cost.

            Returns
            -------
            shrink_at_cost : :class:`decimal.Decimal`
                The value lost to shrink if calculated at cost
        """
        return (D(self.shrink_quantity) *
                self.calculate_purchased_value_per_unit())

    def calculate_shrink_at_potential(self):
        """
            Calculates the amount lost to shrink in potential sales.

            Returns
            -------
            shrink_at_cost : :class:`decimal.Decimal`
                The value lost to shrink in potential sales
        """
        return D(self.shrink_quantity) * self.calculate_sold_value_per_unit()

    def calculate_profit(self):
        """
            Calculates amount recovered through sales that exceeds
            the purchase price

            Returns
            -------
            profit : :class:`decimal.Decimal`
                Value recovered that exceeds value traded for quantity
        """
        return max(0, self.total_recovered - self.purchase_price)

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

    @property
    def purchase_price(self):
        """
            Total value of this item at purchase.

            Returns
            -------
            purchase_price : :class:`decimal.Decimal`
                The total amount paid for this item
        """
        return abs(sum(t.delta_balance for t in self.inbound_transactions))

    @property
    def total_recovered(self):
        """
            Total value recovered through sales of this item

            Returns
            -------
            total_recovered : :class:`decimal.Decimal`
                Sum of all outbound delta_balance for this item
        """
        return sum(t.delta_balance for t in self.outbound_transactions)

    @property
    def total_acquired(self):
        """
            Total number of units acquired over all time

            Returns
            -------
            total : `float`
                Sum of delta_quantity for inbound_transactions
        """
        return sum(t.delta_quantity for t in self.inbound_transactions)

    @property
    def total_sold(self):
        """
            Total number of units sold over all time

            Returns
            -------
            total : `float`
                Sum of delta_quantity for outbound_transactions
        """
        return abs(sum(t.delta_quantity for t in self.outbound_transactions))

    @property
    def shrink_quantity(self):
        """
            Total number of units 'lost' in NIL transactions

            Returns
            -------
            total : `float`
                Sum of delta_quantity for transactions where delta_balance = 0.
        """
        return abs(sum(t.delta_quantity for t in
                       self.transactions.filter(delta_balance=0)))

    @property
    def markup_scheme(self):
        """
            Rendered markup scheme

            Returns
            -------
            markup_scheme : `string`
                e.g. 1@15,3@35,7@80,...
        """
        def generate_tiers():
            t = self.total_acquired
            p = sum((abs(t.delta_balance) for t in self.inbound_transactions))
            while t > 1:
                t = t / self.markup_decay
                p = (p / self.markup_decay) * D(self.markup_growth)
                r = D(int(p) / float(self.markup_nearest))
                r = D((ceil(r) if r % p > 1 else r)) * D(self.markup_nearest)
                yield "%.1f@%.2f" % (t, r)
        return ",".join(list(generate_tiers()))


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

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"

    @classmethod
    def get_list_url(self):
        return reverse('inventory:account_list')

    def get_absolute_url(self):
        return reverse('inventory:account_detail', kwargs=dict(pk=self.pk))

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

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ["-timestamp"]

    @classmethod
    def get_list_url(self):
        return reverse('inventory:transaction_list')

    def get_absolute_url(self):
        return reverse('inventory:transaction_detail', kwargs=dict(pk=self.pk))

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

    class Meta:
        verbose_name = "Purchaser"
        verbose_name_plural = "Purchasers"

    @classmethod
    def get_list_url(self):
        return reverse('inventory:purchaser_list')

    def get_absolute_url(self):
        return reverse('inventory:purchaser_detail', kwargs=dict(pk=self.pk))

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

    def calculate_expenses(self):
        """
            Sums the transaction balances where this purchaser was the seller

            Returns
            -------
            calculated_expenses : :class:`decimal.Decimal`
                The sum of transaction.delta_balance for which this purchaser
                was the seller
        """
        return sum([t.delta_balance for t in
                    Transaction.objects.filter(purchaser=self)
                    if t.delta_balance < 0])

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

    def calculate_accumulation(self):
        """
            Sums the transaction quantities where this purchaser was the seller

            Returns
            -------
            calculated_accumulation : `float`
                The sume of transaction.delta_quantity for which this purchaser
                was the seller
        """
        return abs(sum([t.delta_quantity for t in
                        Transaction.objects.filter(purchaser=self)
                        if t.delta_quantity > 0]))
