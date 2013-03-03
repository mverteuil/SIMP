"""
    :platform: Unix, OS X
    :synopsis: Django views for Inventory viewing & editing.

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
import json

from django.http import HttpResponse
from django.http import HttpResponseRedirect

from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.base import View
from django.views.generic.detail import BaseDetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView


class SectionMixin(object):
    def get_context_data(self, **kwargs):
        context = super(SectionMixin, self).get_context_data(**kwargs)
        context['section'] = self.model.__name__.lower()
        return context


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


class DeleteView(View):
    """
        Model-pluggable template for deleting model instances

        To use:
            In urls.py, call the class method `as_view()` with
            a `model` keyword argument
    """
    model = None

    def get(self, request, pk=None, **kwargs):
        self.model.objects.get(pk=pk).delete()
        return HttpResponseRedirect(self.model.get_list_url())


class SectionListView(SectionMixin, ListView):
    pass


class SectionDetailView(SectionMixin, DetailView):
    pass


class SectionCreateView(SectionMixin, CreateView):
    pass


class SectionUpdateView(SectionMixin, UpdateView):
    pass


class MarkupDetailView(MarkupResponseMixin, BaseDetailView):
    pass
