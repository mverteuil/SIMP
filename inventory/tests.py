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
    def test_calculated_balance(self):
        """ Value should be equal to the sum of transactions """
        assert self.account.calculate_balance() == D("125.00")


class InventoryItemTest(BasicSetup, TestCase):
    def test_calculated_quantity(self):
        """ Value should be equal to the sum of transactions """
        assert self.item.calculate_quantity() == 0


class PurchaserTest(BasicSetup, TestCase):
    def test_calculated_income(self):
        assert self.seller.calculate_income() == 0
        assert self.buyer.calculate_income() == 50

    def test_calculated_consumption(self):
        assert self.seller.calculate_consumption() == 0
        assert self.buyer.calculate_consumption() == 50
