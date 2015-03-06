from django import template
from django.core.urlresolvers import reverse


register = template.Library()


@register.filter('debug')
def debug(obj):
    assert False, obj


@register.filter
def in_group(user, groups):
    """ Checks if user is member of groups. """
    return bool(user.groups.filter(name__in=groups.split(',')).values('name'))


@register.filter
def urlify(name):
    """ Returns url with the `name`. """
    return reverse(name)
