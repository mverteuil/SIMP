from decimal import Decimal as D

from django.db import models


class InventoryItem(models.Model):
    name = models.CharField(verbose_name="Name",
                            max_length=64,
                            blank=False)
    markup_scheme = models.CharField(verbose_name="Markup Scheme",
                                     max_length=64,
                                     blank=True)

    def __unicode__(self):
        return self.name


class Account(models.Model):
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
    item = models.ForeignKey("InventoryItem",
                             related_name="transactions",
                             null=True)
    account = models.ForeignKey("Account",
                                related_name="transactions",
                                null=True)
    purchaser = models.ForeignKey("Purchaser",
                                  related_name="transactions",
                                  null=True)
    delta_quantity = models.FloatField(verbose_name="Delta Quantity",
                                       default=0.0)
    delta_balance = models.DecimalField(verbose_name="Delta Balance",
                                        max_digits=8,
                                        decimal_places=2,
                                        default=D('0.00'))

    def __unicode__(self):
        if self.delta_balance < 0:
            code = "INB"
        elif self.delta_balance == 0:
            code = "NIL"
        else:
            code = "OUT"
        return "%s | %s | %s | %s@%s" % (code, self.account.name,
                                         self.item.name, self.delta_quantity,
                                         self.delta_balance)


class Purchaser(models.Model):
    name = models.CharField(verbose_name="Name",
                            max_length=64,
                            blank=False)

    def __unicode__(self):
        return self.name
