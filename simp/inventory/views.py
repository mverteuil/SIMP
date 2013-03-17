"""
    :platform: Unix, OS X
    :synopsis: Django views for Inventory viewing & editing.

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
import json

from bootstrap.views import (CreateView as BaseCreateView,
                             UpdateView as BaseUpdateView)

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
                initial.update({'delta_quantity': quantity, 'delta_balance': balance})
        return initial
