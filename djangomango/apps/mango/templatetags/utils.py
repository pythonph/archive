from django import template


register = template.Library()


@register.filter('debug')
def debug(obj):
    assert False, obj
