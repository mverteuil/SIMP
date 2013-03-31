"""
    :platform: Unix, OS X
    :synopsis: Django views for Inventory viewing & editing.

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
import json

from bootstrap.views import (CreateView as BaseCreateView,
                             ListView as BaseListView)

from django.http import HttpResponse
from django.views.generic.detail import BaseDetailView

from .models import (Account,
                     InventoryItem,
                     Purchaser)


class MarkupResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'markup_scheme' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        item = context.get('object')
        return json.dumps(item.markup_scheme)


class MarkupDetailView(MarkupResponseMixin, BaseDetailView):
    pass


class CreateView(BaseCreateView):
    def get_initial(self):
        initial = super(CreateView, self).get_initial()
        if self.request.method == "GET":
            account_id = self.request.GET.get('a')
            item_id = self.request.GET.get('i')
            purchaser_id = self.request.GET.get('p')
            quantity = self.request.GET.get('q')
            balance = self.request.GET.get('b')
            if item_id:
                item = InventoryItem.objects.get(pk=item_id)
                initial.update({'item': item})
            if account_id:
                account = Account.objects.get(pk=account_id)
                initial.update({'account': account})
            if purchaser_id:
                purchaser = Purchaser.objects.get(pk=purchaser_id)
                initial.update({'purchaser': purchaser})
            if quantity or balance:
                initial.update({'delta_quantity': quantity,
                                'delta_balance': balance})
        return initial


class ItemListView(BaseListView):
    def get_queryset(self):
        """ Sort the queryset by decreasing quantities """
        quantity_q = InventoryItem.objects.extra(
            select={
                'quantity': ("SELECT SUM(inventory_transaction.delta_quantity) "
                             "FROM inventory_transaction WHERE "
                             "inventory_transaction.item_id = "
                             "inventory_inventoryitem.id")
            }
        )
        quantity_q = quantity_q.order_by("-quantity")
        return quantity_q


class PurchaserListView(BaseListView):
    def get_queryset(self):
        group_by = self.request.GET.get('group_by')
        if group_by:
            if group_by == "buyer":
                return Purchaser.objects.filter(
                    transactions__delta_balance__gt=0).distinct()
            elif group_by == "seller":
                return Purchaser.objects.filter(
                    transactions__delta_balance__lt=0).distinct()
        return Purchaser.objects.all()
