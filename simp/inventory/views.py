"""
    :platform: Unix, OS X
    :synopsis: Django views for Inventory viewing & editing.

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
import json

from django.http import HttpResponse

from django.views.generic.detail import BaseDetailView


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
