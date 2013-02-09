"""
    :platform: Unix, OS X
    :synopsis: Inventory tests

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from decimal import Decimal as D

from django.test import TestCase

from inventory.models import Account
from inventory.models import InventoryItem
from inventory.models import Purchaser
from inventory.models import Transaction


class BasicSetup(object):
    """ Helper mixin class for a basic database setup """
    def setUp(self):
        super(BasicSetup, self).setUp()
        self.account = Account.objects.create(
            name="Test Account",
            initial_balance=D("100.00"),
        )
        self.item = InventoryItem.objects.create(
            name="Test Item",
            markup_scheme="1@5.00,5@4.00",
        )
        self.seller = Purchaser.objects.create(name="Test Seller")
        self.buyer = Purchaser.objects.create(name="Test Buyer")
        self.buy_transaction = Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.seller,
            delta_quantity=50,
            delta_balance=D("-25.00"),
        )
        self.sell_transaction = Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.buyer,
            delta_quantity=-50,
            delta_balance=D("50.00"),
        )

    def tearDown(self):
        super(BasicSetup, self).tearDown()
        for model in (Account, InventoryItem, Purchaser, Transaction):
            model.objects.all().delete()


class AccountTest(BasicSetup, TestCase):
    def test_unicode(self):
        """ Should return name when cast as unicode """
        assert unicode(self.account) == self.account.name

    def test_calculated_balance(self):
        """ Should calculate balance equal to the sum of transactions """
        assert self.account.calculate_balance() == D("125.00")


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
        assert self.item.calculate_quantity() == 0

    def test_calculated_purchased_value_per_unit(self):
        assert self.item.calculate_purchased_value_per_unit() == 0.5
        Transaction.objects.create(
            item=self.item,
            account=self.account,
            purchaser=self.seller,
            delta_quantity=100,
            delta_balance=D("-75.00"),
        )
        assert self.item.calculate_purchased_value_per_unit() == 0.625

    def test_calculated_sold_value_per_unit(self):
        assert self.item.calculate_sold_value_per_unit() == 1
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
        assert self.item.calculate_sold_value_per_unit() == 1.125

    def test_inbound_transactions(self):
        """ Should provide transactions filtered for inbound """
        num_inbound = Transaction.objects.filter(delta_quantity__gt=0).count()
        assert len(self.item.inbound_transactions) == num_inbound

    def test_outbound_transactions(self):
        """ Should provide transactions filtered for outbound/nil """
        num_outbound = Transaction.objects.filter(delta_quantity__lt=0).count()
        assert len(self.item.outbound_transactions) == num_outbound


class PurchaserTest(BasicSetup, TestCase):
    def test_calculated_income(self):
        assert self.seller.calculate_income() == 0
        assert self.buyer.calculate_income() == 50

    def test_calculated_consumption(self):
        assert self.seller.calculate_consumption() == 0
        assert self.buyer.calculate_consumption() == 50
