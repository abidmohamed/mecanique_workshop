from django import template

register = template.Library()


@register.filter
def index(indexable, item):
    return indexable.index(item)
