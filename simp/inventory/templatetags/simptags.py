"""
    :platform: Unix, OS X
    :synopsis: Template Helpers

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from django import template


register = template.Library()


@register.filter
def render_markup_scheme(schema):
    """ Formats the markup scheme for easy review """
    return "".join([
        "<span class='markup-bubble'>%s</span>" % scheme
        for scheme in schema.split(",")])
