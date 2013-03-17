"""
    :platform: Unix, OS X
    :synopsis: Template Helpers

    .. moduleauthor:: Matthew de Verteuil <mverteuil@github.com>
"""
from django import template
from django.core.urlresolvers import reverse


register = template.Library()


def generate_markup_link_list(item):
    """
        Generates a list of tuples, each tuple containing a link to create a
        new transaction at the markup rate specified as well as a string
        representation of that markup rate
    """
    if ',' in item.markup_scheme:
        for rate in reversed(item.markup_scheme.split(',')):
            link = "%s?i=%s&q=-%s&b=%s" % (reverse('inventory:transaction_form'),
                                          item.pk,
                                          rate.split('@')[0],
                                          rate.split('@')[1])
            yield (link, rate)


@register.filter
def render_markup_scheme(item):
    """ Formats the markup scheme for easy review """
    return "".join([
        '<a href="%s" class="btn btn-mini">%s</a>' % (link, label)
        for link, label in generate_markup_link_list(item)])


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
