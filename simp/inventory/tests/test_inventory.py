"""
    :platform: Unix, OS X
    :synopsis: Inventory tests

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from decimal import Decimal as D

from django.test import TestCase

from simp.inventory.models import Account
from simp.inventory.models import InventoryItem as Item
from simp.inventory.models import Purchaser
from simp.inventory.models import Transaction


class BasicSetup(object):
    """ Helper mixin class for a basic database setup """
    def setUp(self):
        super(BasicSetup, self).setUp()
        self.account = Account.objects.create(
            name="Test Account",
            initial_balance=D("100.00"),
        )
        self.item = Item.objects.create(
            name="Test Item",
        )
        self.seller = Purchaser.objects.create(name="Test Seller")
        self.buyer = Purchaser.objects.create(name="Test Buyer")
        self.buy_transaction = Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.seller,
            delta_quantity=50,
            delta_balance=D("-250.00"),
        )
        self.sell_transaction = Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.buyer,
            delta_quantity=-50,
            delta_balance=D("500.00"),
        )

    def tearDown(self):
        super(BasicSetup, self).tearDown()
        for model in (Account, Item, Purchaser, Transaction):
            model.objects.all().delete()


class AccountTest(BasicSetup, TestCase):
    def test_unicode(self):
        """ Should return name when cast as unicode """
        assert unicode(self.account) == self.account.name

    def test_calculated_balance(self):
        """ Should calculate balance equal to the sum of transactions """
        assert self.account.balance == D("350.00")


class InventoryItemTest(BasicSetup, TestCase):
    def test_unicode(self):
        """ Should return name when cast as unicode """
        assert unicode(self.item) == self.item.name

    def test_acquired(self):
        """ Should determine the date acquired """
        assert len(self.item.acquired) == 1
        assert self.item.acquired[0] == self.buy_transaction.timestamp

    def test_calculated_quantity(self):
        """ Should provide quantity as sum of transactions """
        assert self.item.quantity == 0

    def test_calculated_purchased_value_per_unit(self):
        assert self.item.purchased_value_per_unit == 5
        Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.seller,
            delta_quantity=100,
            delta_balance=D("-75.00"),
        )
        self.item = Item.objects.get(pk=self.item.pk)
        total = sum((abs(t.delta_balance)
                     for t in self.item.inbound_transactions))
        total /= D(self.item.total_acquired)
        assert self.item.purchased_value_per_unit == total

    def test_calculated_sold_value_per_unit(self):
        assert self.item.sold_value_per_unit == 10
        # No more inventory, buy some more
        Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.seller,
            delta_quantity=100,
            delta_balance=D("-75.00"),
        )
        # Second sale
        Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.buyer,
            delta_quantity=(-60),
            delta_balance=D("75.00"),
        )
        self.item = Item.objects.get(pk=self.item.pk)
        total = sum(abs(t.delta_balance)
                    for t in self.item.outbound_transactions)
        total /= D(self.item.total_sold)
        assert self.item.sold_value_per_unit == total

    def test_inbound_transactions(self):
        """ Should provide transactions filtered for inbound """
        num_inbound = Transaction.objects.filter(delta_quantity__gt=0).count()
        assert len(self.item.inbound_transactions) == num_inbound

    def test_outbound_transactions(self):
        """ Should provide transactions filtered for outbound/nil """
        num_outbound = Transaction.objects.filter(delta_quantity__lt=0).count()
        assert len(self.item.outbound_transactions) == num_outbound

    def test_total_acquired(self):
        """ Should provide sum of quantities for inbound transactions """
        total = sum(t.delta_quantity for t in self.item.inbound_transactions)
        assert self.item.total_acquired == total

    def test_total_sold(self):
        """ Should provide sum of quantities for outbound transactions """
        total = sum(t.delta_quantity for t in self.item.outbound_transactions)
        assert self.item.total_sold + total == 0

    def test_shrink_quantity(self):
        """ Should provide sum of quantities where balance was zero """
        Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.seller,
            delta_quantity=100,
            delta_balance=D("0.00"),
        )
        total = abs(sum(t.delta_quantity for t in
                    self.item.transactions.filter(delta_balance=0)))
        assert self.item.shrink_quantity == total

    def test_minimum_potential_value(self):
        """
            Should calculate potential with the product of sold vpu and total
            acquired
        """
        potential = self.item.purchased_value_per_unit
        potential *= D(self.item.total_acquired)
        assert self.item.potential_value[0] == potential

    def test_maximum_potential_value(self):
        markup_scheme = [D(t.split('@')[1]) / D(t.split('@')[0])
                         for t in self.item.markup_scheme.split(',')
                         if D(t.split('@')[0]) > 0 and D(t.split('@')[1]) > 0]
        potential = sorted(set(markup_scheme))[-1] * self.item.total_acquired
        assert self.item.potential_value[-1] == potential

    def test_purchase_price(self):
        """ Should calculate own purchase price """
        purchase_price = D(250)
        assert self.item.purchase_price == purchase_price

    def test_shrink_costs(self):
        """ Should calculate shrink costs """
        at_cost = in_potential = D(self.item.shrink_quantity)
        at_cost *= self.item.purchased_value_per_unit
        in_potential *= self.item.sold_value_per_unit
        assert self.item.shrink_at_cost == at_cost
        assert self.item.shrink_at_potential == at_cost

    def test_total_recovered(self):
        """ Should calculated costs recovered through sales """
        recovered = sum(t.delta_balance for t in self.item.outbound_transactions)
        assert self.item.total_recovered == recovered

    def test_profit(self):
        """ Should calculate amount recovered that exceeds costs """
        profit = max(0, self.item.total_recovered - self.item.purchase_price)
        assert self.item.profit == profit

    def test_automatic_markup(self):
        """
            Should automatically calculate markup scheme based on control
            variables (decay, growth and nearest)
        """
        round_five = Item.objects.create(
            name="Oranges",
            markup_decay=2,
            markup_growth=1.06,
            markup_nearest=5,
        )
        round_ten = Item.objects.create(
            name="Apples",
            markup_decay=2,
            markup_growth=1.06,
            markup_nearest=10,
        )
        # Initially no scheme, because no transactions, but it shouldn't
        # explode
        assert not round_five.markup_scheme
        assert not round_ten.markup_scheme
        # Create an inbound transaction to apply the formula to
        acquisition = Transaction.objects.create(
            item=round_five,
            account=self.account,
            purchaser=self.seller,
            delta_quantity=200,
            delta_balance=D(-2000),
        )
        round_five = Item.objects.get(pk=round_five.pk)
        round_five = round_five.markup_scheme
        assert round_five
        round_five = round_five.split(',')
        assert len(round_five) == 8
        assert "50.0@565.00" in round_five
        assert "0.8@15.00" in round_five
        for quantity, price in [t.split('@') for t in round_five]:
            assert len(quantity.split('.')[1]) < 2
            assert float(price) % 5 == 0
        # Use the same transaction for round 10 calculation
        acquisition.item = round_ten
        acquisition.save()

        round_ten = Item.objects.get(pk=round_ten.pk)
        round_ten = round_ten.markup_scheme
        assert round_ten
        round_ten = round_ten.split(',')
        assert len(round_ten) == 8
        assert "50.0@570.00" in round_ten
        assert "0.8@20.00" in round_ten
        for quantity, price in [t.split('@') for t in round_ten]:
            assert len(quantity.split('.')[1]) < 2
            assert float(price) % 10 == 0


class PurchaserTest(BasicSetup, TestCase):
    def test_calculated_income(self):
        assert self.seller.income == 0
        assert self.buyer.income == 500

    def test_calculated_expenses(self):
        assert self.seller.expenses == -250
        assert self.buyer.expenses == 0

    def test_calculated_consumption(self):
        assert self.seller.consumption == 0
        assert self.buyer.consumption == 50

    def test_calculated_accumulation(self):
        assert self.seller.accumulation == 50
        assert self.buyer.accumulation == 0
