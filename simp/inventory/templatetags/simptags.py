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

@register.filter
def clone_transaction_querystring(transaction):
    """
        Returns the query string for adding a new transaction with properties
        equal to the one supplied
    """
    query = []
    query.append('?i=%s' % transaction.item.pk)
    query.append('a=%s' % transaction.account.pk)
    if transaction.purchaser:
        query.append('p=%s' % transaction.purchaser.pk)
    query.append('q=%s' % transaction.delta_quantity)
    query.append('b=%s' % transaction.delta_balance)
    return "&".join(query)
